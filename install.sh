#!/bin/bash

# Script de Instalação Rápida - Sistema de Gestão de Loja
# Para Moçambique

echo "=========================================="
echo "Sistema de Gestão de Loja - Moçambique"
echo "Instalação Rápida"
echo "=========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Por favor, instale o Python 3.8 ou superior."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Verificar PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "❌ PostgreSQL não encontrado."
    echo "Por favor, instale o PostgreSQL antes de continuar:"
    echo "  Ubuntu/Debian: sudo apt install postgresql postgresql-contrib"
    echo "  CentOS/RHEL: sudo yum install postgresql-server"
    exit 1
fi

echo "✅ PostgreSQL encontrado"

# Criar ambiente virtual
echo ""
echo "📦 Criando ambiente virtual..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Erro ao criar ambiente virtual"
    exit 1
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências"
    exit 1
fi

# Configurar .env
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Configurando ambiente..."
    cp .env.example .env
    
    echo ""
    echo "Por favor, configure o arquivo .env com suas informações:"
    echo "  1. Credenciais do banco de dados"
    echo "  2. Dados da sua empresa"
    echo "  3. Chave secreta (SECRET_KEY)"
    echo ""
    read -p "Pressione ENTER após configurar o .env..."
fi

# Criar banco de dados
echo ""
echo "🗄️  Configurando banco de dados..."
echo ""
echo "Por favor, execute os seguintes comandos no PostgreSQL:"
echo "  sudo -u postgres psql"
echo "  CREATE DATABASE loja_gestao_mz;"
echo "  CREATE USER seu_usuario WITH PASSWORD 'sua_senha';"
echo "  GRANT ALL PRIVILEGES ON DATABASE loja_gestao_mz TO seu_usuario;"
echo "  \\q"
echo ""
read -p "Pressione ENTER após criar o banco de dados..."

# Inicializar banco
echo ""
echo "🔧 Inicializando banco de dados..."
python init_db.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Erro ao inicializar banco de dados"
    echo "Verifique as credenciais no arquivo .env"
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Instalação concluída com sucesso!"
echo "=========================================="
echo ""
echo "Para iniciar o sistema:"
echo "  1. Ative o ambiente virtual: source venv/bin/activate"
echo "  2. Execute: python app.py"
echo "  3. Acesse: http://localhost:5000"
echo ""
echo "Credenciais padrão:"
echo "  Email: admin@loja.co.mz"
echo "  Senha: admin123"
echo ""
echo "⚠️  IMPORTANTE: Altere a senha após o primeiro login!"
echo "=========================================="
