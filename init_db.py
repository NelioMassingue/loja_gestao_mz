"""
Script para inicializar o banco de dados e criar usuário admin padrão
"""
from app import create_app
from models import db, Usuario, Categoria
from config import config
import sys

def init_db():
    """Inicializa o banco de dados"""
    app = create_app('development')
    
    with app.app_context():
        print("Criando tabelas do banco de dados...")
        db.create_all()
        
        # Verificar se já existe usuário admin
        admin = Usuario.query.filter_by(email='admin@loja.co.mz').first()
        
        if not admin:
            print("\nCriando usuário administrador padrão...")
            admin = Usuario(
                nome='Administrador',
                email='admin@loja.co.mz',
                tipo='admin',
                ativo=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            print("\n" + "="*60)
            print("USUÁRIO ADMINISTRADOR CRIADO COM SUCESSO!")
            print("="*60)
            print("Email: admin@loja.co.mz")
            print("Senha: admin123")
            print("\n⚠️  IMPORTANTE: Altere a senha após o primeiro login!")
            print("="*60 + "\n")
        else:
            print("\nUsuário administrador já existe.")
        
        # Criar categorias padrão
        categorias_padrao = [
            'Alimentação',
            'Bebidas',
            'Higiene e Limpeza',
            'Eletrônicos',
            'Vestuário',
            'Outros'
        ]
        
        for nome_cat in categorias_padrao:
            if not Categoria.query.filter_by(nome=nome_cat).first():
                categoria = Categoria(nome=nome_cat, descricao=f'Categoria {nome_cat}')
                db.session.add(categoria)
                print(f"Categoria '{nome_cat}' criada.")
        
        db.session.commit()
        print("\n✅ Banco de dados inicializado com sucesso!")
        print("\nPara iniciar o sistema, execute:")
        print("  python app.py")
        print("\nEm seguida, acesse: http://localhost:5000\n")

if __name__ == '__main__':
    try:
        init_db()
    except Exception as e:
        print(f"\n❌ Erro ao inicializar banco de dados: {str(e)}")
        print("\nVerifique se:")
        print("  1. O PostgreSQL está instalado e em execução")
        print("  2. O banco de dados 'loja_gestao_mz' foi criado")
        print("  3. As credenciais no arquivo .env estão corretas")
        print("\nComandos PostgreSQL:")
        print("  sudo -u postgres psql")
        print("  CREATE DATABASE loja_gestao_mz;")
        print("  CREATE USER seu_usuario WITH PASSWORD 'sua_senha';")
        print("  GRANT ALL PRIVILEGES ON DATABASE loja_gestao_mz TO seu_usuario;")
        sys.exit(1)
