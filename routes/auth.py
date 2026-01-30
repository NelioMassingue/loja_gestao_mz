from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Usuario

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        lembrar = request.form.get('lembrar') == 'on'
        
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_password(senha):
            if not usuario.ativo:
                flash('Usuário inativo. Entre em contato com o administrador.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(usuario, remember=lembrar)
            next_page = request.args.get('next')
            flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
            return redirect(next_page if next_page else url_for('dashboard.index'))
        else:
            flash('Email ou senha incorretos.', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Você saiu do sistema com sucesso.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/perfil')
@login_required
def perfil():
    """Página de perfil do usuário"""
    return render_template('auth/perfil.html')

@auth_bp.route('/alterar-senha', methods=['POST'])
@login_required
def alterar_senha():
    """Alterar senha do usuário"""
    senha_atual = request.form.get('senha_atual')
    senha_nova = request.form.get('senha_nova')
    senha_confirmacao = request.form.get('senha_confirmacao')
    
    if not current_user.check_password(senha_atual):
        flash('Senha atual incorreta.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    if senha_nova != senha_confirmacao:
        flash('A nova senha e a confirmação não coincidem.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    if len(senha_nova) < 6:
        flash('A senha deve ter pelo menos 6 caracteres.', 'danger')
        return redirect(url_for('auth.perfil'))
    
    current_user.set_password(senha_nova)
    db.session.commit()
    flash('Senha alterada com sucesso!', 'success')
    return redirect(url_for('auth.perfil'))
