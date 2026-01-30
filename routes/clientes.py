from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from models import db, Cliente

clientes_bp = Blueprint('clientes', __name__, url_prefix='/clientes')

@clientes_bp.route('/')
@login_required
def listar():
    """Lista todos os clientes"""
    page = request.args.get('page', 1, type=int)
    busca = request.args.get('busca', '')
    
    query = Cliente.query
    
    if busca:
        query = query.filter(
            db.or_(
                Cliente.nome.ilike(f'%{busca}%'),
                Cliente.cpf_nuit.ilike(f'%{busca}%'),
                Cliente.telefone.ilike(f'%{busca}%')
            )
        )
    
    clientes = query.order_by(Cliente.nome).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('clientes/listar.html', clientes=clientes, busca=busca)

@clientes_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo():
    """Cadastrar novo cliente"""
    if request.method == 'POST':
        try:
            cliente = Cliente(
                nome=request.form.get('nome'),
                cpf_nuit=request.form.get('cpf_nuit'),
                email=request.form.get('email'),
                telefone=request.form.get('telefone'),
                endereco=request.form.get('endereco'),
                cidade=request.form.get('cidade'),
                observacoes=request.form.get('observacoes')
            )
            
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente cadastrado com sucesso!', 'success')
            return redirect(url_for('clientes.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar cliente: {str(e)}', 'danger')
    
    return render_template('clientes/form.html', cliente=None)

@clientes_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar(id):
    """Editar cliente existente"""
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            cliente.nome = request.form.get('nome')
            cliente.cpf_nuit = request.form.get('cpf_nuit')
            cliente.email = request.form.get('email')
            cliente.telefone = request.form.get('telefone')
            cliente.endereco = request.form.get('endereco')
            cliente.cidade = request.form.get('cidade')
            cliente.observacoes = request.form.get('observacoes')
            cliente.ativo = request.form.get('ativo') == 'on'
            
            db.session.commit()
            flash('Cliente atualizado com sucesso!', 'success')
            return redirect(url_for('clientes.listar'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar cliente: {str(e)}', 'danger')
    
    return render_template('clientes/form.html', cliente=cliente)

@clientes_bp.route('/<int:id>')
@login_required
def detalhes(id):
    """Detalhes do cliente"""
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/detalhes.html', cliente=cliente)
