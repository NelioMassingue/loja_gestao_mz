import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base da aplicação"""
    
    # Chave secreta para sessões
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:postgres@localhost:5432/loja_gestao_mz'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=1)
    SESSION_TYPE = 'filesystem'
    
    # Configuração de upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
    
    # Configurações da empresa
    EMPRESA_NOME = os.environ.get('EMPRESA_NOME') or 'Loja Moçambique'
    EMPRESA_ENDERECO = os.environ.get('EMPRESA_ENDERECO') or 'Maputo, Moçambique'
    EMPRESA_TELEFONE = os.environ.get('EMPRESA_TELEFONE') or '+258 XX XXX XXXX'
    EMPRESA_EMAIL = os.environ.get('EMPRESA_EMAIL') or 'contato@loja.co.mz'
    EMPRESA_NUIT = os.environ.get('EMPRESA_NUIT') or '000000000'
    
    # Moeda
    MOEDA = 'MZN'
    MOEDA_SIMBOLO = 'MT'
    
    # Paginação
    ITEMS_PER_PAGE = 20

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configurações de teste"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/loja_gestao_test'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
