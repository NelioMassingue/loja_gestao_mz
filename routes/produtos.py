from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Produto, Categoria, Fornecedor, MovimentoEstoque
from werkzeug.utils import secure_filename
import os

produtos_bp = Blueprint('produtos', __name__, url_prefix='/produtos')

@produtos_bp.route('/')
@login_required
def listar():
    """Lista todos os produtos"""
    page = request.args.get('page', 1, type=int)
    busca = request.args.get('busca', '')
    categoria_id = request.args.get('categoria', type=int)
    
    query = Produto.query
    
    if busca:
        query = query.filter(
            db.or_(
                Produto.nome.ilike(f'%{busca}%'),
                Produto.codigo.ilike(f'%{busca}%')
            )
        )
    
    if categoria_id:
        query = query.filter_by(categoria_id=categoria_id)
    
    produtos = query.order_by(Produto.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    categorias = Categoria.query.filter_by(ativo=True).order_by(Categoria.nome).all()
    
    return render_template('produtos/listar.html', 
                         produtos=produtos, 
                         categorias=categorias,
                         busca=busca,
                         categoria_id=categoria_id)

@produtos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cadastrar novo produto"""
    if request.method == 'POST':
        try:
            produto = Produto(
                codigo=request.form.get('codigo'),
                nome=request.form.get('nome'),
                descricao=request.form.get('descricao'),
                categoria_id=request.form.get('categoria_id') or None,
                fornecedor_id=request.form.get('fornecedor_id') or None,
                preco_custo=float(request.form.get('preco_custo', 0)),
                preco_venda=float(request.form.get('preco_venda', 0)),
                estoque_atual=int(request.form.get('estoque_inicial', 0)),
                estoque_minimo=int(request.form.get('estoque_minimo', 0)),
                unidade_medida=request.form.get('unidade_medida', 'UN')
            )
            
            db.session.add(produto)
            db.session.flush()
            
            # Registrar movimento de estoque inicial
            if produto.estoque_atual > 0:
                movimento = MovimentoEstoque(
                    produto_id=produto.id,
                    tipo='entrada',
                    quantidade=produto.estoque_atual,
                    estoque_anterior=0,
                    estoque_atual=produto.estoque_atual,
                    motivo='Estoque inicial',
                    usuario_id=current_user.id
                )
                db.session.add(movimento)
            
            db.session.commit()
            flash('Produto cadastrado com sucesso!', 'success')
            return redirect(url_for('produtos.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar produto: {str(e)}', 'danger')
    
    categorias = Categoria.query.filter_by(ativo=True).order_by(Categoria.nome).all()
    fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome).all()
    
    return render_template('produtos/form.html', 
                         produto=None, 
                         categorias=categorias,
                         fornecedores=fornecedores)

@produtos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar produto existente"""
    produto = Produto.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            produto.codigo = request.form.get('codigo')
            produto.nome = request.form.get('nome')
            produto.descricao = request.form.get('descricao')
            produto.categoria_id = request.form.get('categoria_id') or None
            produto.fornecedor_id = request.form.get('fornecedor_id') or None
            produto.preco_custo = float(request.form.get('preco_custo', 0))
            produto.preco_venda = float(request.form.get('preco_venda', 0))
            produto.estoque_minimo = int(request.form.get('estoque_minimo', 0))
            produto.unidade_medida = request.form.get('unidade_medida', 'UN')
            produto.ativo = request.form.get('ativo') == 'on'
            
            db.session.commit()
            flash('Produto atualizado com sucesso!', 'success')
            return redirect(url_for('produtos.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar produto: {str(e)}', 'danger')
    
    categorias = Categoria.query.filter_by(ativo=True).order_by(Categoria.nome).all()
    fornecedores = Fornecedor.query.filter_by(ativo=True).order_by(Fornecedor.nome).all()
    
    return render_template('produtos/form.html', 
                         produto=produto, 
                         categorias=categorias,
                         fornecedores=fornecedores)

@produtos_bp.route('/<int:id>/deletar', methods=['POST'])
@login_required
def deletar(id):
    """Deletar produto"""
    produto = Produto.query.get_or_404(id)
    
    try:
        produto.ativo = False
        db.session.commit()
        flash('Produto desativado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao desativar produto: {str(e)}', 'danger')
    
    return redirect(url_for('produtos.listar'))

@produtos_bp.route('/api/buscar')
@login_required
def api_buscar():
    """API para buscar produtos (usado no PDV)"""
    termo = request.args.get('termo', '')
    
    if len(termo) < 2:
        return jsonify([])
    
    produtos = Produto.query.filter(
        Produto.ativo == True,
        db.or_(
            Produto.nome.ilike(f'%{termo}%'),
            Produto.codigo.ilike(f'%{termo}%')
        )
    ).limit(10).all()
    
    resultado = [{
        'id': p.id,
        'codigo': p.codigo,
        'nome': p.nome,
        'preco_venda': float(p.preco_venda),
        'estoque_atual': p.estoque_atual,
        'unidade_medida': p.unidade_medida
    } for p in produtos]
    
    return jsonify(resultado)

@produtos_bp.route('/categorias')
@login_required
def categorias():
    """Gerenciar categorias"""
    categorias = Categoria.query.order_by(Categoria.nome).all()
    return render_template('produtos/categorias.html', categorias=categorias)

@produtos_bp.route('/categorias/nova', methods=['POST'])
@login_required
def nova_categoria():
    """Cadastrar nova categoria"""
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    
    if not nome:
        flash('Nome da categoria é obrigatório.', 'danger')
        return redirect(url_for('produtos.categorias'))
    
    try:
        categoria = Categoria(nome=nome, descricao=descricao)
        db.session.add(categoria)
        db.session.commit()
        flash('Categoria cadastrada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar categoria: {str(e)}', 'danger')
    
    return redirect(url_for('produtos.categorias'))
