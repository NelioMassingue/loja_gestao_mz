# Sistema de Gestão de Loja - Moçambique

Sistema completo de gestão comercial desenvolvido em Python/Flask com PostgreSQL, especialmente projetado para o mercado moçambicano.

## 🚀 Funcionalidades

### Módulos Principais

1. **Dashboard**
   - Visão geral de vendas
   - Indicadores de desempenho
   - Gráficos e estatísticas
   - Produtos mais vendidos

2. **PDV (Ponto de Venda)**
   - Interface rápida e intuitiva
   - Busca de produtos em tempo real
   - Múltiplas formas de pagamento (Dinheiro, Cartão, M-Pesa, E-Mola)
   - Aplicação de descontos
   - Impressão de recibos

3. **Gestão de Produtos**
   - Cadastro completo de produtos
   - Controle por categorias
   - Gestão de preços (custo e venda)
   - Cálculo automático de margem de lucro
   - Imagens de produtos
   - Código de barras

4. **Controle de Estoque**
   - Entrada e saída de produtos
   - Histórico de movimentações
   - Alertas de estoque mínimo
   - Ajustes manuais

5. **Gestão de Clientes**
   - Cadastro completo
   - Histórico de compras
   - Dados de contato

6. **Gestão de Fornecedores**
   - Cadastro com NUIT
   - Controle de produtos por fornecedor
   - Dados de contato

7. **Controle de Caixa**
   - Abertura e fechamento de caixa
   - Movimentações financeiras
   - Relatório por forma de pagamento
   - Histórico de caixas

8. **Relatórios**
   - Relatório de vendas
   - Produtos mais vendidos
   - Clientes que mais compram
   - Exportação em PDF
   - Filtros por período

## 📋 Requisitos

- Python 3.8+
- PostgreSQL 12+
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Clonar o Repositório
```bash
git clone [seu-repositorio]
cd loja_gestao_mz
```

### 2. Criar Ambiente Virtual
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL

Acesse o PostgreSQL:
```bash
sudo -u postgres psql
```

Execute os comandos:
```sql
CREATE DATABASE loja_gestao_mz;
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE loja_gestao_mz TO seu_usuario;
\q
```

### 5. Configurar Variáveis de Ambiente

Copie o arquivo de exemplo:
```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas configurações:
```env
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/loja_gestao_mz
SECRET_KEY=gere-uma-chave-secreta-forte-aqui
EMPRESA_NOME=Nome da Sua Loja
EMPRESA_ENDERECO=Seu Endereço, Cidade
EMPRESA_TELEFONE=+258 XX XXX XXXX
EMPRESA_EMAIL=contato@sualoja.co.mz
EMPRESA_NUIT=Seu NUIT
```

### 6. Inicializar Banco de Dados
```bash
python init_db.py
```

Este comando irá:
- Criar todas as tabelas
- Criar usuário administrador padrão
- Criar categorias padrão

**Credenciais padrão:**
- Email: `admin@loja.co.mz`
- Senha: `admin123`

⚠️ **IMPORTANTE**: Altere a senha após o primeiro login!

### 7. Executar a Aplicação
```bash
python app.py
```

Acesse: `http://localhost:5000`

## 📱 Uso do Sistema

### Primeiro Acesso

1. Acesse `http://localhost:5000`
2. Faça login com as credenciais padrão
3. Vá em "Perfil" e altere sua senha
4. Configure os dados da empresa em `.env`

### Fluxo de Trabalho Recomendado

1. **Cadastrar Categorias**
   - Acesse Produtos → Categorias
   - Crie as categorias necessárias

2. **Cadastrar Fornecedores**
   - Acesse Fornecedores
   - Adicione seus fornecedores

3. **Cadastrar Produtos**
   - Acesse Produtos → Novo Produto
   - Preencha todas as informações
   - Defina estoque inicial

4. **Abrir Caixa**
   - Acesse Caixa
   - Clique em "Abrir Caixa"
   - Informe o saldo inicial

5. **Realizar Vendas**
   - Acesse PDV - Vendas
   - Busque os produtos
   - Finalize a venda

6. **Fechar Caixa**
   - Acesse Caixa
   - Revise as movimentações
   - Clique em "Fechar Caixa"

## 🎨 Personalização

### Alterar Tema/Cores

Edite o arquivo `templates/base.html` na seção `<style>`:

```css
:root {
    --primary-color: #2c3e50;      /* Cor principal */
    --secondary-color: #3498db;    /* Cor secundária */
    --success-color: #27ae60;      /* Verde (sucesso) */
    --danger-color: #e74c3c;       /* Vermelho (erro) */
    --warning-color: #f39c12;      /* Amarelo (aviso) */
}
```

### Adicionar Novo Usuário

Execute o Python interativo:
```bash
python
```

```python
from app import create_app
from models import db, Usuario

app = create_app()
with app.app_context():
    usuario = Usuario(
        nome='Nome do Usuário',
        email='usuario@email.com',
        tipo='vendedor',  # admin, gerente, vendedor
        ativo=True
    )
    usuario.set_password('senha123')
    db.session.add(usuario)
    db.session.commit()
    print('Usuário criado com sucesso!')
```

## 🔐 Níveis de Acesso

- **Admin**: Acesso total ao sistema
- **Gerente**: Acesso a relatórios e gestão
- **Vendedor**: Acesso ao PDV e consultas

## 🐛 Solução de Problemas

### Erro de Conexão com Banco de Dados

Verifique:
1. PostgreSQL está rodando: `sudo systemctl status postgresql`
2. Credenciais corretas no `.env`
3. Banco de dados existe: `psql -U postgres -l`

### Erro ao Importar Módulos

```bash
pip install -r requirements.txt --upgrade
```

### Porta 5000 já em uso

Altere a porta em `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📊 Backup do Banco de Dados

### Fazer Backup
```bash
pg_dump -U seu_usuario loja_gestao_mz > backup.sql
```

### Restaurar Backup
```bash
psql -U seu_usuario loja_gestao_mz < backup.sql
```

## 🚀 Deploy em Produção

### Recomendações

1. Use servidor web (Gunicorn, uWSGI)
2. Configure proxy reverso (Nginx, Apache)
3. Use HTTPS
4. Desabilite modo DEBUG
5. Use variáveis de ambiente para senhas
6. Configure backups automáticos
7. Implemente logs

### Exemplo com Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Licença

Este sistema foi desenvolvido para comercialização em Moçambique.

## 🤝 Suporte

Para suporte e dúvidas, entre em contato através do email configurado no sistema.

## 🔄 Atualizações Futuras

- [ ] Integração com APIs de pagamento móvel (M-Pesa, E-Mola)
- [ ] App móvel (Android/iOS)
- [ ] Impressão de código de barras
- [ ] Multi-loja
- [ ] Integração com sistemas de contabilidade
- [ ] NFC-e / Faturação eletrónica

## 📞 Contatos Úteis Moçambique

- **M-Pesa**: https://www.mpesa.co.mz
- **E-Mola**: https://www.e-mola.com
- **AT (Autoridade Tributária)**: https://www.at.gov.mz

---

**Desenvolvido para o mercado moçambicano** 🇲🇿
