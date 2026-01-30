from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Caixa, MovimentoCaixa
from datetime import datetime
from sqlalchemy import func

caixa_bp = Blueprint('caixa', __name__, url_prefix='/caixa')

@caixa_bp.route('/')
@login_required
def index():
    """Página principal do caixa"""
    caixa_aberto = Caixa.query.filter_by(status='aberto').first()
    
    if caixa_aberto:
        # Calcular totais
        movimentos = MovimentoCaixa.query.filter_by(caixa_id=caixa_aberto.id).all()
        
        total_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
        total_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
        saldo_atual = caixa_aberto.saldo_inicial + total_entradas - total_saidas
        
        # Agrupar por forma de pagamento
        formas_pagamento = db.session.query(
            MovimentoCaixa.forma_pagamento,
            func.sum(MovimentoCaixa.valor).label('total')
        ).filter(
            MovimentoCaixa.caixa_id == caixa_aberto.id,
            MovimentoCaixa.tipo == 'entrada'
        ).group_by(MovimentoCaixa.forma_pagamento).all()
        
        return render_template('caixa/aberto.html',
                             caixa=caixa_aberto,
                             movimentos=movimentos,
                             total_entradas=total_entradas,
                             total_saidas=total_saidas,
                             saldo_atual=saldo_atual,
                             formas_pagamento=formas_pagamento)
    
    # Histórico de caixas
    caixas = Caixa.query.order_by(Caixa.data_abertura.desc()).limit(10).all()
    return render_template('caixa/index.html', caixas=caixas)

@caixa_bp.route('/abrir', methods=['POST'])
@login_required
def abrir():
    """Abrir novo caixa"""
    # Verificar se já existe caixa aberto
    caixa_aberto = Caixa.query.filter_by(status='aberto').first()
    if caixa_aberto:
        flash('Já existe um caixa aberto.', 'warning')
        return redirect(url_for('caixa.index'))
    
    try:
        saldo_inicial = float(request.form.get('saldo_inicial', 0))
        
        # Gerar número do caixa
        ultimo_caixa = Caixa.query.order_by(Caixa.id.desc()).first()
        numero_caixa = f"CX{(ultimo_caixa.id + 1):06d}" if ultimo_caixa else "CX000001"
        
        caixa = Caixa(
            numero_caixa=numero_caixa,
            usuario_abertura_id=current_user.id,
            saldo_inicial=saldo_inicial,
            status='aberto'
        )
        
        db.session.add(caixa)
        db.session.commit()
        
        flash(f'Caixa {numero_caixa} aberto com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao abrir caixa: {str(e)}', 'danger')
    
    return redirect(url_for('caixa.index'))

@caixa_bp.route('/fechar', methods=['POST'])
@login_required
def fechar():
    """Fechar caixa aberto"""
    caixa = Caixa.query.filter_by(status='aberto').first()
    
    if not caixa:
        flash('Nenhum caixa está aberto.', 'warning')
        return redirect(url_for('caixa.index'))
    
    try:
        # Calcular saldo final
        movimentos = MovimentoCaixa.query.filter_by(caixa_id=caixa.id).all()
        total_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
        total_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
        saldo_final = caixa.saldo_inicial + total_entradas - total_saidas
        
        caixa.saldo_final = saldo_final
        caixa.data_fechamento = datetime.utcnow()
        caixa.usuario_fechamento_id = current_user.id
        caixa.status = 'fechado'
        caixa.observacoes = request.form.get('observacoes')
        
        db.session.commit()
        flash(f'Caixa {caixa.numero_caixa} fechado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao fechar caixa: {str(e)}', 'danger')
    
    return redirect(url_for('caixa.index'))

@caixa_bp.route('/movimento/adicionar', methods=['POST'])
@login_required
def adicionar_movimento():
    """Adicionar movimento manual ao caixa"""
    caixa = Caixa.query.filter_by(status='aberto').first()
    
    if not caixa:
        flash('Nenhum caixa está aberto.', 'warning')
        return redirect(url_for('caixa.index'))
    
    try:
        movimento = MovimentoCaixa(
            caixa_id=caixa.id,
            tipo=request.form.get('tipo'),
            valor=float(request.form.get('valor')),
            forma_pagamento=request.form.get('forma_pagamento'),
            descricao=request.form.get('descricao'),
            usuario_id=current_user.id
        )
        
        db.session.add(movimento)
        db.session.commit()
        
        flash('Movimento adicionado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao adicionar movimento: {str(e)}', 'danger')
    
    return redirect(url_for('caixa.index'))

@caixa_bp.route('/<int:id>')
@login_required
def detalhes(id):
    """Detalhes de um caixa fechado"""
    caixa = Caixa.query.get_or_404(id)
    movimentos = MovimentoCaixa.query.filter_by(caixa_id=caixa.id).all()
    
    total_entradas = sum(m.valor for m in movimentos if m.tipo == 'entrada')
    total_saidas = sum(m.valor for m in movimentos if m.tipo == 'saida')
    
    return render_template('caixa/detalhes.html',
                         caixa=caixa,
                         movimentos=movimentos,
                         total_entradas=total_entradas,
                         total_saidas=total_saidas)
