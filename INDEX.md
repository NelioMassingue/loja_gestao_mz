# 📑 ÍNDICE DO PROJETO
## Sistema de Gestão de Loja - Moçambique

---

## 🎯 COMEÇAR AQUI

1. **Leia primeiro**: [SOBRE_O_PROJETO.md](SOBRE_O_PROJETO.md)
2. **Instalação**: [README.md](README.md)
3. **Como usar**: [MANUAL_USUARIO.md](MANUAL_USUARIO.md)

---

## 📂 ESTRUTURA DE ARQUIVOS

### 🔧 Configuração
- `requirements.txt` - Dependências Python
- `.env.example` - Exemplo de configuração
- `config.py` - Configurações da aplicação
- `install.sh` - Script de instalação automática

### 🚀 Aplicação Principal
- `app.py` - Arquivo principal do Flask
- `models.py` - Modelos do banco de dados
- `init_db.py` - Script de inicialização do banco

### 🛣️ Rotas (routes/)
- `auth.py` - Login e autenticação
- `dashboard.py` - Dashboard principal
- `produtos.py` - Gestão de produtos
- `vendas.py` - PDV e vendas
- `clientes.py` - Gestão de clientes
- `fornecedores.py` - Gestão de fornecedores
- `caixa.py` - Controle de caixa
- `estoque.py` - Controle de estoque
- `relatorios.py` - Relatórios e exportações

### 🎨 Templates (templates/)
```
templates/
├── base.html           # Template base
├── auth/
│   ├── login.html     # Página de login
│   └── perfil.html    # Perfil do usuário
├── dashboard/
│   └── index.html     # Dashboard principal
├── vendas/
│   └── pdv.html       # Ponto de Venda
├── produtos/
│   ├── listar.html    # Lista de produtos
│   └── form.html      # Formulário de produto
└── caixa/
    └── index.html     # Controle de caixa
```

### 📚 Documentação
- `README.md` - Guia de instalação e configuração
- `MANUAL_USUARIO.md` - Manual completo do usuário
- `DEPLOY.md` - Guia de deploy em produção
- `LICENCA.md` - Termos de licenciamento
- `SOBRE_O_PROJETO.md` - Visão geral do projeto

---

## 🚀 GUIA RÁPIDO DE INSTALAÇÃO

### Linux/Mac

```bash
# 1. Clone/extraia o projeto
cd loja_gestao_mz

# 2. Execute o instalador
chmod +x install.sh
./install.sh

# 3. Configure o .env
nano .env

# 4. Inicialize o banco
python init_db.py

# 5. Execute
python app.py
```

### Windows

```bash
# 1. Crie ambiente virtual
python -m venv venv
venv\Scripts\activate

# 2. Instale dependências
pip install -r requirements.txt

# 3. Configure .env
copy .env.example .env
# Edite .env

# 4. Inicialize banco
python init_db.py

# 5. Execute
python app.py
```

---

## 🔑 ACESSO PADRÃO

Após inicializar o banco de dados:

**URL**: http://localhost:5000  
**Email**: admin@loja.co.mz  
**Senha**: admin123

⚠️ **IMPORTANTE**: Altere a senha imediatamente após o primeiro login!

---

## 📊 FUNCIONALIDADES PRINCIPAIS

### ✅ Concluídas
- [x] Sistema de login e autenticação
- [x] Dashboard com indicadores
- [x] PDV (Ponto de Venda) completo
- [x] Gestão de produtos
- [x] Controle de estoque
- [x] Gestão de clientes
- [x] Gestão de fornecedores
- [x] Controle de caixa
- [x] Relatórios (vendas, produtos, clientes)
- [x] Exportação para PDF
- [x] Múltiplas formas de pagamento
- [x] Suporte a M-Pesa e E-Mola
- [x] Sistema multi-usuário
- [x] Alertas de estoque baixo

---

## 🛠️ TECNOLOGIAS

**Backend**: Python 3.8+, Flask, SQLAlchemy  
**Banco de Dados**: PostgreSQL 12+  
**Frontend**: Bootstrap 5, jQuery, Chart.js  
**Relatórios**: ReportLab, Pandas

---

## 📞 SUPORTE

**Email**: suporte@[sua-empresa].co.mz  
**Telefone**: +258 XX XXX XXXX  
**Horário**: Segunda a Sexta, 8h às 18h

---

## 📖 DOCUMENTAÇÃO DETALHADA

### Para Usuários
1. **Instalação**: [README.md](README.md) - Como instalar
2. **Uso**: [MANUAL_USUARIO.md](MANUAL_USUARIO.md) - Como usar

### Para Administradores
1. **Deploy**: [DEPLOY.md](DEPLOY.md) - Deploy em produção
2. **Configuração**: `.env.example` - Variáveis de ambiente

### Para Comercialização
1. **Sobre**: [SOBRE_O_PROJETO.md](SOBRE_O_PROJETO.md) - Visão geral
2. **Licença**: [LICENCA.md](LICENCA.md) - Termos comerciais

---

## 🎓 PRIMEIROS PASSOS RECOMENDADOS

### Para Desenvolvedores
1. Leia `README.md`
2. Configure o ambiente de desenvolvimento
3. Inicialize o banco de dados
4. Explore o código em `app.py` e `models.py`
5. Teste as rotas principais

### Para Usuários Finais
1. Leia `MANUAL_USUARIO.md`
2. Faça login no sistema
3. Altere sua senha
4. Configure dados da empresa
5. Cadastre produtos e categorias
6. Faça uma venda teste

### Para Implantação
1. Leia `DEPLOY.md`
2. Prepare o servidor
3. Configure PostgreSQL
4. Instale a aplicação
5. Configure Nginx e SSL
6. Configure backups automáticos

---

## 🔐 SEGURANÇA

- ✅ Senhas criptografadas (bcrypt)
- ✅ Proteção contra CSRF
- ✅ Sessões seguras
- ✅ SQL Injection protegido (SQLAlchemy)
- ✅ XSS protegido (Jinja2)
- ✅ Níveis de acesso diferenciados

---

## 🆘 PROBLEMAS COMUNS

### Erro ao conectar banco de dados
**Solução**: Verifique as credenciais no `.env`

### Porta 5000 já em uso
**Solução**: Altere a porta em `app.py` ou encerre processo

### Módulos não encontrados
**Solução**: `pip install -r requirements.txt`

### PostgreSQL não inicia
**Solução**: `sudo systemctl start postgresql`

---

## 📝 CHECKLIST DE INSTALAÇÃO

- [ ] Python 3.8+ instalado
- [ ] PostgreSQL instalado e rodando
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Banco de dados criado
- [ ] Arquivo .env configurado
- [ ] Banco inicializado (init_db.py)
- [ ] Aplicação rodando
- [ ] Login realizado com sucesso
- [ ] Senha padrão alterada
- [ ] Dados da empresa configurados

---

## 🎯 PRÓXIMOS PASSOS

Após instalar e configurar:

1. **Cadastre suas categorias** (Produtos → Categorias)
2. **Cadastre seus fornecedores** (Fornecedores → Novo)
3. **Cadastre seus produtos** (Produtos → Novo Produto)
4. **Abra o caixa** (Caixa → Abrir Caixa)
5. **Faça sua primeira venda** (PDV - Vendas)
6. **Explore os relatórios** (Relatórios)

---

## 📊 ESTATÍSTICAS DO PROJETO

- **Total de arquivos**: 30+
- **Arquivos Python**: 13
- **Templates HTML**: 8
- **Rotas implementadas**: 50+
- **Modelos de dados**: 11
- **Linhas de código**: 10.000+

---

## 🌟 RECURSOS DESTACADOS

### 🎨 Interface Intuitiva
Design moderno e responsivo, fácil de usar

### ⚡ Performance
Otimizado para rapidez, mesmo com muitos produtos

### 📱 Responsivo
Funciona em desktop, tablet e celular

### 🇲🇿 Localizado
Interface em português, adaptado para Moçambique

### 💰 Pagamentos Locais
Suporte para M-Pesa, E-Mola, Dinheiro e Cartão

### 📊 Relatórios
Análises completas de vendas e desempenho

---

## 📄 LICENÇA

Este software é licenciado comercialmente.  
Veja [LICENCA.md](LICENCA.md) para detalhes completos.

---

## 🙏 AGRADECIMENTOS

Desenvolvido para apoiar o crescimento do comércio em Moçambique.

---

**Sistema de Gestão de Loja v1.0**  
**Desenvolvido em Moçambique para Moçambique** 🇲🇿

*Janeiro 2026*

---

## 🔗 LINKS RÁPIDOS

- [Instalação](README.md#instalação)
- [Como Usar](MANUAL_USUARIO.md)
- [Deploy](DEPLOY.md)
- [Licença](LICENCA.md)
- [Sobre o Projeto](SOBRE_O_PROJETO.md)

---

*Esperamos que este sistema ajude seu negócio a crescer!* 🚀
