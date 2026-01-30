from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Venda, ItemVenda, Produto, Cliente, MovimentoEstoque, Caixa, MovimentoCaixa
from datetime import datetime

vendas_bp = Blueprint('vendas', __name__, url_prefix='/vendas')

@vendas_bp.route('/')
@login_required
def listar():
    """Lista todas as vendas"""
    page = request.args.get('page', 1, type=int)
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    query = Venda.query
    
    if data_inicio:
        query = query.filter(Venda.data_venda >= datetime.strptime(data_inicio, '%Y-%m-%d'))
    if data_fim:
        query = query.filter(Venda.data_venda <= datetime.strptime(data_fim, '%Y-%m-%d'))
    
    vendas = query.order_by(Venda.data_venda.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('vendas/listar.html', vendas=vendas)

@vendas_bp.route('/<int:id>')
@login_required
def detalhes(id):
    """Detalhes de uma venda"""
    venda = Venda.query.get_or_404(id)
    return render_template('vendas/detalhes.html', venda=venda)

@vendas_bp.route('/pdv')
@login_required
def pdv():
    """Ponto de Venda (PDV)"""
    # Verificar se há caixa aberto
    caixa_aberto = Caixa.query.filter_by(status='aberto').first()
    
    if not caixa_aberto:
        flash('Nenhum caixa está aberto. Por favor, abra um caixa primeiro.', 'warning')
        return redirect(url_for('caixa.index'))
    
    clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    return render_template('vendas/pdv.html', clientes=clientes, caixa=caixa_aberto)

@vendas_bp.route('/processar', methods=['POST'])
@login_required
def processar_venda():
    """Processar uma nova venda"""
    try:
        data = request.get_json()
        
        # Verificar caixa aberto
        caixa_aberto = Caixa.query.filter_by(status='aberto').first()
        if not caixa_aberto:
            return jsonify({'success': False, 'error': 'Nenhum caixa está aberto'}), 400
        
        # Validar itens
        if not data.get('itens') or len(data['itens']) == 0:
            return jsonify({'success': False, 'error': 'Nenhum item na venda'}), 400
        
        # Gerar número da venda
        ultima_venda = Venda.query.order_by(Venda.id.desc()).first()
        numero_venda = f"VND{(ultima_venda.id + 1):06d}" if ultima_venda else "VND000001"
        
        # Criar venda
        venda = Venda(
            numero_venda=numero_venda,
            cliente_id=data.get('cliente_id') or None,
            vendedor_id=current_user.id,
            subtotal=float(data['subtotal']),
            desconto=float(data.get('desconto', 0)),
            total=float(data['total']),
            forma_pagamento=data['forma_pagamento'],
            observacoes=data.get('observacoes')
        )
        
        db.session.add(venda)
        db.session.flush()
        
        # Processar itens da venda
        for item_data in data['itens']:
            produto = Produto.query.get(item_data['produto_id'])
            
            if not produto:
                db.session.rollback()
                return jsonify({'success': False, 'error': f'Produto {item_data["produto_id"]} não encontrado'}), 400
            
            if produto.estoque_atual < item_data['quantidade']:
                db.session.rollback()
                return jsonify({'success': False, 'error': f'Estoque insuficiente para {produto.nome}'}), 400
            
            # Criar item da venda
            item = ItemVenda(
                venda_id=venda.id,
                produto_id=produto.id,
                quantidade=item_data['quantidade'],
                preco_unitario=float(item_data['preco_unitario']),
                subtotal=float(item_data['subtotal']),
                desconto=float(item_data.get('desconto', 0)),
                total=float(item_data['total'])
            )
            db.session.add(item)
            
            # Atualizar estoque
            estoque_anterior = produto.estoque_atual
            produto.estoque_atual -= item_data['quantidade']
            
            # Registrar movimento de estoque
            movimento = MovimentoEstoque(
                produto_id=produto.id,
                tipo='saida',
                quantidade=item_data['quantidade'],
                estoque_anterior=estoque_anterior,
                estoque_atual=produto.estoque_atual,
                motivo=f'Venda {numero_venda}',
                usuario_id=current_user.id
            )
            db.session.add(movimento)
        
        # Registrar movimento de caixa
        movimento_caixa = MovimentoCaixa(
            caixa_id=caixa_aberto.id,
            tipo='entrada',
            valor=venda.total,
            forma_pagamento=venda.forma_pagamento,
            descricao=f'Venda {numero_venda}',
            venda_id=venda.id,
            usuario_id=current_user.id
        )
        db.session.add(movimento_caixa)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'venda_id': venda.id,
            'numero_venda': venda.numero_venda,
            'message': 'Venda processada com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@vendas_bp.route('/<int:id>/cancelar', methods=['POST'])
@login_required
def cancelar(id):
    """Cancelar uma venda"""
    venda = Venda.query.get_or_404(id)
    
    if venda.status == 'cancelada':
        flash('Esta venda já foi cancelada.', 'warning')
        return redirect(url_for('vendas.detalhes', id=id))
    
    try:
        # Reverter estoque
        for item in venda.itens:
            produto = item.produto
            estoque_anterior = produto.estoque_atual
            produto.estoque_atual += item.quantidade
            
            # Registrar movimento de estoque
            movimento = MovimentoEstoque(
                produto_id=produto.id,
                tipo='entrada',
                quantidade=item.quantidade,
                estoque_anterior=estoque_anterior,
                estoque_atual=produto.estoque_atual,
                motivo=f'Cancelamento venda {venda.numero_venda}',
                usuario_id=current_user.id
            )
            db.session.add(movimento)
        
        # Atualizar status da venda
        venda.status = 'cancelada'
        
        # Registrar movimento de caixa (saída)
        caixa_aberto = Caixa.query.filter_by(status='aberto').first()
        if caixa_aberto:
            movimento_caixa = MovimentoCaixa(
                caixa_id=caixa_aberto.id,
                tipo='saida',
                valor=venda.total,
                forma_pagamento=venda.forma_pagamento,
                descricao=f'Cancelamento venda {venda.numero_venda}',
                venda_id=venda.id,
                usuario_id=current_user.id
            )
            db.session.add(movimento_caixa)
        
        db.session.commit()
        flash('Venda cancelada com sucesso!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cancelar venda: {str(e)}', 'danger')
    
    return redirect(url_for('vendas.detalhes', id=id))

@vendas_bp.route('/<int:id>/imprimir')
@login_required
def imprimir(id):
    """Imprimir recibo da venda"""
    venda = Venda.query.get_or_404(id)
    return render_template('vendas/recibo.html', venda=venda)
