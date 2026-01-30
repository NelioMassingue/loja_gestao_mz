from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Produto, MovimentoEstoque

estoque_bp = Blueprint('estoque', __name__, url_prefix='/estoque')

@estoque_bp.route('/')
@login_required
def index():
    """Página principal de estoque"""
    page = request.args.get('page', 1, type=int)
    alerta = request.args.get('alerta', '')
    
    query = Produto.query.filter_by(ativo=True)
    
    if alerta == 'baixo':
        query = query.filter(Produto.estoque_atual <= Produto.estoque_minimo)
    
    produtos = query.order_by(Produto.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('estoque/index.html', produtos=produtos, alerta=alerta)

@estoque_bp.route('/movimentos')
@login_required
def movimentos():
    """Histórico de movimentos de estoque"""
    page = request.args.get('page', 1, type=int)
    produto_id = request.args.get('produto_id', type=int)
    tipo = request.args.get('tipo', '')
    
    query = MovimentoEstoque.query
    
    if produto_id:
        query = query.filter_by(produto_id=produto_id)
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    movimentos = query.order_by(MovimentoEstoque.data_movimento.desc()).paginate(
        page=page, per_page=50, error_out=False
    )
    
    produtos = Produto.query.filter_by(ativo=True).order_by(Produto.nome).all()
    
    return render_template('estoque/movimentos.html', 
                         movimentos=movimentos,
                         produtos=produtos,
                         produto_id=produto_id,
                         tipo=tipo)

@estoque_bp.route('/ajustar/<int:produto_id>', methods=['GET', 'POST'])
@login_required
def ajustar(produto_id):
    """Ajustar estoque de um produto"""
    produto = Produto.query.get_or_404(produto_id)
    
    if request.method == 'POST':
        try:
            tipo = request.form.get('tipo')
            quantidade = int(request.form.get('quantidade'))
            motivo = request.form.get('motivo')
            
            if quantidade <= 0:
                flash('A quantidade deve ser maior que zero.', 'danger')
                return redirect(url_for('estoque.ajustar', produto_id=produto_id))
            
            estoque_anterior = produto.estoque_atual
            
            if tipo == 'entrada':
                produto.estoque_atual += quantidade
            elif tipo == 'saida':
                if produto.estoque_atual < quantidade:
                    flash('Estoque insuficiente.', 'danger')
                    return redirect(url_for('estoque.ajustar', produto_id=produto_id))
                produto.estoque_atual -= quantidade
            else:  # ajuste
                produto.estoque_atual = quantidade
            
            # Registrar movimento
            movimento = MovimentoEstoque(
                produto_id=produto.id,
                tipo=tipo,
                quantidade=quantidade,
                estoque_anterior=estoque_anterior,
                estoque_atual=produto.estoque_atual,
                motivo=motivo,
                usuario_id=current_user.id
            )
            
            db.session.add(movimento)
            db.session.commit()
            
            flash('Estoque ajustado com sucesso!', 'success')
            return redirect(url_for('estoque.index'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao ajustar estoque: {str(e)}', 'danger')
    
    return render_template('estoque/ajustar.html', produto=produto)
