from flask import Blueprint, render_template, request, send_file
from flask_login import login_required
from models import db, Venda, ItemVenda, Produto, Cliente
from sqlalchemy import func, extract
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm

relatorios_bp = Blueprint('relatorios', __name__, url_prefix='/relatorios')

@relatorios_bp.route('/')
@login_required
def index():
    """Página principal de relatórios"""
    return render_template('relatorios/index.html')

@relatorios_bp.route('/vendas')
@login_required
def vendas():
    """Relatório de vendas"""
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    formato = request.args.get('formato', 'html')
    
    # Definir período padrão (últimos 30 dias)
    if not data_inicio or not data_fim:
        data_fim = datetime.utcnow()
        data_inicio = data_fim - timedelta(days=30)
    else:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    
    # Buscar vendas
    vendas = Venda.query.filter(
        Venda.data_venda.between(data_inicio, data_fim),
        Venda.status == 'concluida'
    ).order_by(Venda.data_venda.desc()).all()
    
    # Calcular totais
    total_vendas = len(vendas)
    valor_total = sum(v.total for v in vendas)
    ticket_medio = valor_total / total_vendas if total_vendas > 0 else 0
    
    # Vendas por forma de pagamento
    vendas_por_pagamento = db.session.query(
        Venda.forma_pagamento,
        func.count(Venda.id).label('quantidade'),
        func.sum(Venda.total).label('total')
    ).filter(
        Venda.data_venda.between(data_inicio, data_fim),
        Venda.status == 'concluida'
    ).group_by(Venda.forma_pagamento).all()
    
    if formato == 'pdf':
        return gerar_pdf_vendas(vendas, data_inicio, data_fim, total_vendas, valor_total, ticket_medio)
    
    return render_template('relatorios/vendas.html',
                         vendas=vendas,
                         data_inicio=data_inicio,
                         data_fim=data_fim,
                         total_vendas=total_vendas,
                         valor_total=valor_total,
                         ticket_medio=ticket_medio,
                         vendas_por_pagamento=vendas_por_pagamento)

@relatorios_bp.route('/produtos')
@login_required
def produtos():
    """Relatório de produtos mais vendidos"""
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Definir período padrão (últimos 30 dias)
    if not data_inicio or not data_fim:
        data_fim = datetime.utcnow()
        data_inicio = data_fim - timedelta(days=30)
    else:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    
    # Produtos mais vendidos
    produtos_vendidos = db.session.query(
        Produto,
        func.sum(ItemVenda.quantidade).label('quantidade_vendida'),
        func.sum(ItemVenda.total).label('valor_total')
    ).join(ItemVenda).join(Venda).filter(
        Venda.data_venda.between(data_inicio, data_fim),
        Venda.status == 'concluida'
    ).group_by(Produto.id).order_by(
        db.text('quantidade_vendida DESC')
    ).limit(50).all()
    
    return render_template('relatorios/produtos.html',
                         produtos_vendidos=produtos_vendidos,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

@relatorios_bp.route('/clientes')
@login_required
def clientes():
    """Relatório de clientes"""
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    
    # Definir período padrão (últimos 30 dias)
    if not data_inicio or not data_fim:
        data_fim = datetime.utcnow()
        data_inicio = data_fim - timedelta(days=30)
    else:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
    
    # Clientes que mais compraram
    clientes_top = db.session.query(
        Cliente,
        func.count(Venda.id).label('total_compras'),
        func.sum(Venda.total).label('valor_total')
    ).join(Venda).filter(
        Venda.data_venda.between(data_inicio, data_fim),
        Venda.status == 'concluida'
    ).group_by(Cliente.id).order_by(
        db.text('valor_total DESC')
    ).limit(50).all()
    
    return render_template('relatorios/clientes.html',
                         clientes_top=clientes_top,
                         data_inicio=data_inicio,
                         data_fim=data_fim)

def gerar_pdf_vendas(vendas, data_inicio, data_fim, total_vendas, valor_total, ticket_medio):
    """Gerar PDF do relatório de vendas"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    titulo = Paragraph(f"<b>Relatório de Vendas</b><br/>{data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}", styles['Title'])
    elements.append(titulo)
    elements.append(Spacer(1, 0.5*cm))
    
    # Resumo
    resumo_data = [
        ['Total de Vendas:', str(total_vendas)],
        ['Valor Total:', f"{valor_total:,.2f} MT"],
        ['Ticket Médio:', f"{ticket_medio:,.2f} MT"]
    ]
    resumo_table = Table(resumo_data, colWidths=[8*cm, 8*cm])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ]))
    elements.append(resumo_table)
    elements.append(Spacer(1, 1*cm))
    
    # Tabela de vendas
    vendas_data = [['Nº Venda', 'Data', 'Cliente', 'Total']]
    for venda in vendas[:50]:  # Limitar a 50 vendas
        vendas_data.append([
            venda.numero_venda,
            venda.data_venda.strftime('%d/%m/%Y'),
            venda.cliente.nome if venda.cliente else 'Cliente não informado',
            f"{venda.total:,.2f}"
        ])
    
    vendas_table = Table(vendas_data, colWidths=[3*cm, 3*cm, 7*cm, 3*cm])
    vendas_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(vendas_table)
    
    doc.build(elements)
    buffer.seek(0)
    
    return send_file(
        buffer,
        as_attachment=True,
        download_name=f'relatorio_vendas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
        mimetype='application/pdf'
    )
