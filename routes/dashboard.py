from flask import Blueprint, render_template
from flask_login import login_required
from models import db, Produto, Cliente, Venda, Usuario
from sqlalchemy import func, extract
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def index():
    """Dashboard principal"""
    hoje = datetime.utcnow().date()
    inicio_mes = datetime(hoje.year, hoje.month, 1)
    
    # Estatísticas gerais
    total_produtos = Produto.query.filter_by(ativo=True).count()
    total_clientes = Cliente.query.filter_by(ativo=True).count()
    produtos_estoque_baixo = Produto.query.filter(
        Produto.ativo == True,
        Produto.estoque_atual <= Produto.estoque_minimo
    ).count()
    
    # Vendas do dia
    vendas_hoje = db.session.query(func.sum(Venda.total)).filter(
        func.date(Venda.data_venda) == hoje,
        Venda.status == 'concluida'
    ).scalar() or 0
    
    # Vendas do mês
    vendas_mes = db.session.query(func.sum(Venda.total)).filter(
        Venda.data_venda >= inicio_mes,
        Venda.status == 'concluida'
    ).scalar() or 0
    
    # Últimas vendas
    ultimas_vendas = Venda.query.filter_by(status='concluida').order_by(
        Venda.data_venda.desc()
    ).limit(10).all()
    
    # Produtos mais vendidos
    produtos_mais_vendidos = db.session.query(
        Produto,
        func.sum(db.text('itens_venda.quantidade')).label('total_vendido')
    ).join(
        db.text('itens_venda'), Produto.id == db.text('itens_venda.produto_id')
    ).join(
        Venda, db.text('itens_venda.venda_id') == Venda.id
    ).filter(
        Venda.status == 'concluida',
        Venda.data_venda >= inicio_mes
    ).group_by(Produto.id).order_by(
        db.text('total_vendido DESC')
    ).limit(5).all()
    
    # Vendas por dia (últimos 7 dias)
    vendas_por_dia = []
    for i in range(6, -1, -1):
        dia = hoje - timedelta(days=i)
        total = db.session.query(func.sum(Venda.total)).filter(
            func.date(Venda.data_venda) == dia,
            Venda.status == 'concluida'
        ).scalar() or 0
        vendas_por_dia.append({
            'dia': dia.strftime('%d/%m'),
            'total': float(total)
        })
    
    return render_template('dashboard/index.html',
                         total_produtos=total_produtos,
                         total_clientes=total_clientes,
                         produtos_estoque_baixo=produtos_estoque_baixo,
                         vendas_hoje=vendas_hoje,
                         vendas_mes=vendas_mes,
                         ultimas_vendas=ultimas_vendas,
                         produtos_mais_vendidos=produtos_mais_vendidos,
                         vendas_por_dia=vendas_por_dia)
