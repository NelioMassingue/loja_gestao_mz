# 🏪 Sistema de Gestão de Loja - Moçambique

## Visão Geral

Sistema completo de gestão comercial desenvolvido especialmente para o mercado moçambicano, com suporte a métodos de pagamento locais e interface em português.

---

## 🎯 Objetivo

Fornecer uma solução completa, profissional e acessível para pequenas e médias empresas em Moçambique gerenciarem suas operações comerciais de forma eficiente.

---

## ✨ Principais Características

### 💰 Financeiro
- Suporte para Metical (MT)
- M-Pesa integrado
- E-Mola integrado
- Controle de caixa diário
- Múltiplas formas de pagamento

### 📦 Gestão de Produtos
- Cadastro ilimitado de produtos
- Controle por categorias
- Códigos de barras
- Gestão de estoque automática
- Alertas de estoque mínimo
- Cálculo de margem de lucro

### 🛒 Ponto de Venda (PDV)
- Interface rápida e intuitiva
- Busca inteligente de produtos
- Aplicação de descontos
- Impressão de recibos
- Suporte a múltiplos operadores

### 📊 Relatórios e Análises
- Dashboard com indicadores
- Relatórios de vendas
- Produtos mais vendidos
- Análise de clientes
- Exportação em PDF
- Gráficos interativos

### 👥 Gestão de Clientes
- Cadastro completo
- Histórico de compras
- Dados de contato
- Observações personalizadas

### 🚚 Gestão de Fornecedores
- Cadastro com NUIT
- Controle de produtos por fornecedor
- Histórico de compras

### 📦 Controle de Estoque
- Entrada e saída
- Histórico de movimentações
- Ajustes manuais
- Rastreabilidade completa

### 🔐 Segurança
- Sistema multi-usuário
- Três níveis de acesso
- Senhas criptografadas
- Logs de atividades

---

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**: Linguagem principal
- **Flask**: Framework web
- **SQLAlchemy**: ORM para banco de dados
- **PostgreSQL**: Banco de dados robusto
- **Flask-Login**: Autenticação
- **Flask-Migrate**: Migrações de banco

### Frontend
- **Bootstrap 5**: Framework CSS
- **JavaScript/jQuery**: Interatividade
- **Chart.js**: Gráficos
- **Bootstrap Icons**: Ícones

### Relatórios
- **ReportLab**: Geração de PDFs
- **Pandas**: Análise de dados
- **openpyxl**: Exportação Excel

---

## 📁 Estrutura do Projeto

```
loja_gestao_mz/
├── app.py                 # Aplicação principal
├── config.py             # Configurações
├── models.py             # Modelos de banco de dados
├── init_db.py           # Script de inicialização
├── requirements.txt      # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
├── routes/              # Rotas da aplicação
│   ├── auth.py         # Autenticação
│   ├── dashboard.py    # Dashboard
│   ├── produtos.py     # Gestão de produtos
│   ├── vendas.py       # PDV e vendas
│   ├── clientes.py     # Gestão de clientes
│   ├── fornecedores.py # Gestão de fornecedores
│   ├── caixa.py        # Controle de caixa
│   ├── estoque.py      # Controle de estoque
│   └── relatorios.py   # Relatórios
├── templates/           # Templates HTML
│   ├── base.html       # Template base
│   ├── auth/           # Login e perfil
│   ├── dashboard/      # Dashboard
│   ├── produtos/       # Produtos
│   ├── vendas/         # PDV e vendas
│   ├── clientes/       # Clientes
│   ├── fornecedores/   # Fornecedores
│   ├── caixa/          # Caixa
│   ├── estoque/        # Estoque
│   └── relatorios/     # Relatórios
├── static/             # Arquivos estáticos
│   ├── css/           # Estilos
│   ├── js/            # Scripts
│   └── uploads/       # Imagens de produtos
└── docs/              # Documentação
    ├── README.md
    ├── MANUAL_USUARIO.md
    ├── DEPLOY.md
    └── LICENCA.md
```

---

## 🚀 Início Rápido

### Instalação Rápida (Linux)

```bash
# Clone o repositório
git clone [seu-repositorio]
cd loja_gestao_mz

# Execute o instalador
chmod +x install.sh
./install.sh
```

### Instalação Manual

1. **Instale dependências**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. **Configure PostgreSQL**:
```sql
CREATE DATABASE loja_gestao_mz;
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
GRANT ALL PRIVILEGES ON DATABASE loja_gestao_mz TO seu_usuario;
```

3. **Configure .env**:
```bash
cp .env.example .env
# Edite .env com suas configurações
```

4. **Inicialize o banco**:
```bash
python init_db.py
```

5. **Execute**:
```bash
python app.py
```

6. **Acesse**: http://localhost:5000

---

## 📖 Documentação

- **README.md**: Informações gerais e instalação
- **MANUAL_USUARIO.md**: Guia completo do usuário
- **DEPLOY.md**: Guia de implantação em produção
- **LICENCA.md**: Termos de licenciamento

---

## 🎓 Níveis de Acesso

| Nível | Acesso |
|-------|--------|
| **Admin** | Acesso total ao sistema |
| **Gerente** | PDV, relatórios, gestão de produtos/clientes |
| **Vendedor** | Apenas PDV e consultas |

---

## 💡 Casos de Uso

### Pequeno Comércio
- Mini-mercado
- Loja de conveniência
- Padaria
- Farmácia

### Médio Comércio
- Supermercado
- Loja de roupas
- Loja de eletrônicos
- Distribuidora

### Serviços
- Restaurante
- Cafeteria
- Lanchonete
- Barbearia

---

## 🔮 Roadmap Futuro

### Versão 1.1 (Planejado)
- [ ] App móvel Android
- [ ] Leitor de código de barras via câmera
- [ ] Impressora térmica de recibos
- [ ] Integração nativa M-Pesa API

### Versão 1.2 (Planejado)
- [ ] Multi-loja
- [ ] Sincronização em nuvem
- [ ] App iOS
- [ ] Módulo de delivery

### Versão 2.0 (Futuro)
- [ ] Inteligência artificial para previsão de vendas
- [ ] Integração contábil
- [ ] NFC-e / Faturação eletrónica
- [ ] Sistema de fidelidade

---

## 🤝 Contribuições

Este é um produto comercial. Para sugestões e melhorias, entre em contato através dos canais oficiais.

---

## 📞 Suporte

### Canais de Atendimento
- **Email**: suporte@[sua-empresa].co.mz
- **Telefone**: +258 XX XXX XXXX
- **WhatsApp**: +258 XX XXX XXXX
- **Website**: https://www.[sua-empresa].co.mz

### Horário de Atendimento
- Segunda a Sexta: 8h às 18h
- Sábado: 8h às 12h
- Suporte 24/7 disponível para licença empresarial

---

## 📊 Estatísticas do Projeto

- **Linhas de código**: ~10.000+
- **Módulos**: 9 principais
- **Templates**: 20+
- **Rotas**: 50+
- **Tabelas no banco**: 11

---

## 🏆 Diferenciais

✅ **Desenvolvido para Moçambique**: Interface em português, métodos de pagamento locais  
✅ **Código Limpo**: Arquitetura profissional e manutenível  
✅ **Documentação Completa**: Manuais e guias detalhados  
✅ **Suporte Local**: Atendimento em português  
✅ **Preço Acessível**: Mais barato que sistemas importados  
✅ **Personalizável**: Adaptável às necessidades específicas  

---

## 📜 Licença

Este software é licenciado comercialmente. Veja [LICENCA.md](LICENCA.md) para detalhes.

---

## ⭐ Testemunhos

*"Excelente sistema! Muito fácil de usar e atende perfeitamente nossas necessidades."*  
— Cliente Satisfeito, Maputo

*"O suporte é rápido e eficiente. Recomendo!"*  
— Cliente Satisfeito, Matola

---

**Desenvolvido com ❤️ em Moçambique para Moçambique** 🇲🇿

*Sistema de Gestão de Loja - Versão 1.0 - Janeiro 2026*
