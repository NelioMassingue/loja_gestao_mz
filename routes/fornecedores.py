from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Fornecedor

fornecedores_bp = Blueprint('fornecedores', __name__, url_prefix='/fornecedores')

@fornecedores_bp.route('/')
@login_required
def listar():
    """Lista todos os fornecedores"""
    page = request.args.get('page', 1, type=int)
    busca = request.args.get('busca', '')
    
    query = Fornecedor.query
    
    if busca:
        query = query.filter(
            db.or_(
                Fornecedor.nome.ilike(f'%{busca}%'),
                Fornecedor.nuit.ilike(f'%{busca}%')
            )
        )
    
    fornecedores = query.order_by(Fornecedor.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('fornecedores/listar.html', fornecedores=fornecedores, busca=busca)

@fornecedores_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cadastrar novo fornecedor"""
    if request.method == 'POST':
        try:
            fornecedor = Fornecedor(
                nome=request.form.get('nome'),
                nuit=request.form.get('nuit'),
                email=request.form.get('email'),
                telefone=request.form.get('telefone'),
                endereco=request.form.get('endereco'),
                cidade=request.form.get('cidade'),
                observacoes=request.form.get('observacoes')
            )
            
            db.session.add(fornecedor)
            db.session.commit()
            flash('Fornecedor cadastrado com sucesso!', 'success')
            return redirect(url_for('fornecedores.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar fornecedor: {str(e)}', 'danger')
    
    return render_template('fornecedores/form.html', fornecedor=None)

@fornecedores_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar fornecedor existente"""
    fornecedor = Fornecedor.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            fornecedor.nome = request.form.get('nome')
            fornecedor.nuit = request.form.get('nuit')
            fornecedor.email = request.form.get('email')
            fornecedor.telefone = request.form.get('telefone')
            fornecedor.endereco = request.form.get('endereco')
            fornecedor.cidade = request.form.get('cidade')
            fornecedor.observacoes = request.form.get('observacoes')
            fornecedor.ativo = request.form.get('ativo') == 'on'
            
            db.session.commit()
            flash('Fornecedor atualizado com sucesso!', 'success')
            return redirect(url_for('fornecedores.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar fornecedor: {str(e)}', 'danger')
    
    return render_template('fornecedores/form.html', fornecedor=fornecedor)
