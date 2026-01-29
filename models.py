from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    """Modelo de usuário do sistema"""
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False, default='vendedor')  # admin, gerente, vendedor
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    vendas = db.relationship('Venda', backref='vendedor', lazy=True)
    movimentos_caixa = db.relationship('MovimentoCaixa', backref='usuario', lazy=True)
    
    def set_password(self, senha):
        """Define a senha do usuário"""
        self.senha_hash = generate_password_hash(senha)
    
    def check_password(self, senha):
        """Verifica a senha do usuário"""
        return check_password_hash(self.senha_hash, senha)
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

class Categoria(db.Model):
    """Modelo de categoria de produtos"""
    __tablename__ = 'categorias'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamentos
    produtos = db.relationship('Produto', backref='categoria', lazy=True)
    
    def __repr__(self):
        return f'<Categoria {self.nome}>'

class Fornecedor(db.Model):
    """Modelo de fornecedor"""
    __tablename__ = 'fornecedores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    nuit = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    cidade = db.Column(db.String(100))
    observacoes = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    produtos = db.relationship('Produto', backref='fornecedor', lazy=True)
    
    def __repr__(self):
        return f'<Fornecedor {self.nome}>'

class Produto(db.Model):
    """Modelo de produto"""
    __tablename__ = 'produtos'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    nome = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedores.id'))
    preco_custo = db.Column(db.Numeric(10, 2), nullable=False)
    preco_venda = db.Column(db.Numeric(10, 2), nullable=False)
    estoque_atual = db.Column(db.Integer, default=0)
    estoque_minimo = db.Column(db.Integer, default=0)
    unidade_medida = db.Column(db.String(20), default='UN')  # UN, KG, L, etc
    imagem = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    itens_venda = db.relationship('ItemVenda', backref='produto', lazy=True)
    movimentos_estoque = db.relationship('MovimentoEstoque', backref='produto', lazy=True)
    
    @property
    def margem_lucro(self):
        """Calcula a margem de lucro"""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0
    
    def __repr__(self):
        return f'<Produto {self.codigo} - {self.nome}>'

class Cliente(db.Model):
    """Modelo de cliente"""
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    cpf_nuit = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120))
    telefone = db.Column(db.String(20))
    endereco = db.Column(db.Text)
    cidade = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    observacoes = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    vendas = db.relationship('Venda', backref='cliente', lazy=True)
    
    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Venda(db.Model):
    """Modelo de venda"""
    __tablename__ = 'vendas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_venda = db.Column(db.String(20), unique=True, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)  # dinheiro, cartao, mpesa, emola
    status = db.Column(db.String(20), default='concluida')  # concluida, cancelada
    observacoes = db.Column(db.Text)
    
    # Relacionamentos
    itens = db.relationship('ItemVenda', backref='venda', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Venda {self.numero_venda}>'

class ItemVenda(db.Model):
    """Modelo de item de venda"""
    __tablename__ = 'itens_venda'
    
    id = db.Column(db.Integer, primary_key=True)
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'), nullable=False)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    desconto = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __repr__(self):
        return f'<ItemVenda {self.id}>'

class MovimentoEstoque(db.Model):
    """Modelo de movimento de estoque"""
    __tablename__ = 'movimentos_estoque'
    
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # entrada, saida, ajuste
    quantidade = db.Column(db.Integer, nullable=False)
    estoque_anterior = db.Column(db.Integer, nullable=False)
    estoque_atual = db.Column(db.Integer, nullable=False)
    motivo = db.Column(db.String(200))
    data_movimento = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    
    def __repr__(self):
        return f'<MovimentoEstoque {self.id}>'

class Caixa(db.Model):
    """Modelo de caixa"""
    __tablename__ = 'caixas'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_caixa = db.Column(db.String(20), unique=True, nullable=False)
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    data_fechamento = db.Column(db.DateTime)
    usuario_abertura_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    usuario_fechamento_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    saldo_inicial = db.Column(db.Numeric(10, 2), default=0)
    saldo_final = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20), default='aberto')  # aberto, fechado
    observacoes = db.Column(db.Text)
    
    # Relacionamentos
    movimentos = db.relationship('MovimentoCaixa', backref='caixa', lazy=True)
    
    def __repr__(self):
        return f'<Caixa {self.numero_caixa}>'

class MovimentoCaixa(db.Model):
    """Modelo de movimento de caixa"""
    __tablename__ = 'movimentos_caixa'
    
    id = db.Column(db.Integer, primary_key=True)
    caixa_id = db.Column(db.Integer, db.ForeignKey('caixas.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # entrada, saida
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    forma_pagamento = db.Column(db.String(50))
    descricao = db.Column(db.String(200))
    venda_id = db.Column(db.Integer, db.ForeignKey('vendas.id'))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_movimento = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<MovimentoCaixa {self.id}>'
