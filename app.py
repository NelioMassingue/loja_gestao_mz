import os
from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from config import config
from models import db, Usuario

# Inicializar extensões
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_name='default'):
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Configurar login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))
    
    # Criar diretórios necessários
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Registrar blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.produtos import produtos_bp
    from routes.vendas import vendas_bp
    from routes.clientes import clientes_bp
    from routes.fornecedores import fornecedores_bp
    from routes.caixa import caixa_bp
    from routes.relatorios import relatorios_bp
    from routes.estoque import estoque_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(produtos_bp)
    app.register_blueprint(vendas_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(fornecedores_bp)
    app.register_blueprint(caixa_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(estoque_bp)
    
    # Rota principal
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    
    # Filtros de template personalizados
    @app.template_filter('moeda')
    def moeda_filter(valor):
        """Formata valor como moeda moçambicana"""
        try:
            return f"{float(valor):,.2f} MT".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return "0,00 MT"
    
    @app.template_filter('data')
    def data_filter(data):
        """Formata data para padrão brasileiro/moçambicano"""
        try:
            return data.strftime('%d/%m/%Y')
        except:
            return ""
    
    @app.template_filter('data_hora')
    def data_hora_filter(data):
        """Formata data e hora"""
        try:
            return data.strftime('%d/%m/%Y %H:%M')
        except:
            return ""
    
    # Contexto global para templates
    @app.context_processor
    def inject_globals():
        return {
            'empresa_nome': app.config['EMPRESA_NOME'],
            'empresa_endereco': app.config['EMPRESA_ENDERECO'],
            'empresa_telefone': app.config['EMPRESA_TELEFONE'],
            'empresa_email': app.config['EMPRESA_EMAIL'],
            'empresa_nuit': app.config['EMPRESA_NUIT'],
            'moeda': app.config['MOEDA'],
            'moeda_simbolo': app.config['MOEDA_SIMBOLO']
        }
    
    return app

if __name__ == '__main__':
    app = create_app(os.getenv('FLASK_ENV', 'development'))
    app.run(host='0.0.0.0', port=5000, debug=True)
