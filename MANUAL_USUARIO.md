# Manual do Usuário
## Sistema de Gestão de Loja - Moçambique

---

## 📖 Índice

1. [Introdução](#introdução)
2. [Acesso ao Sistema](#acesso-ao-sistema)
3. [Dashboard](#dashboard)
4. [PDV - Ponto de Venda](#pdv---ponto-de-venda)
5. [Gestão de Produtos](#gestão-de-produtos)
6. [Controle de Estoque](#controle-de-estoque)
7. [Gestão de Clientes](#gestão-de-clientes)
8. [Gestão de Fornecedores](#gestão-de-fornecedores)
9. [Controle de Caixa](#controle-de-caixa)
10. [Relatórios](#relatórios)
11. [Dicas e Boas Práticas](#dicas-e-boas-práticas)

---

## Introdução

Bem-vindo ao Sistema de Gestão de Loja! Este sistema foi desenvolvido especialmente para o mercado moçambicano, com suporte a métodos de pagamento locais (M-Pesa, E-Mola) e moeda local (Metical - MT).

### Principais Funcionalidades

- ✅ Ponto de Venda (PDV) rápido e intuitivo
- ✅ Controle completo de estoque
- ✅ Gestão de clientes e fornecedores
- ✅ Controle de caixa diário
- ✅ Relatórios e estatísticas
- ✅ Multi-usuário com diferentes níveis de acesso

---

## Acesso ao Sistema

### Primeiro Acesso

1. Abra o navegador e acesse: `http://localhost:5000`
2. Use as credenciais padrão:
   - **Email**: admin@loja.co.mz
   - **Senha**: admin123
3. **IMPORTANTE**: Após o primeiro login, vá em "Perfil" e altere sua senha!

### Níveis de Acesso

- **Administrador**: Acesso completo a todas as funcionalidades
- **Gerente**: Acesso a vendas, produtos, relatórios e configurações
- **Vendedor**: Acesso ao PDV e consulta de produtos/clientes

---

## Dashboard

O Dashboard é a tela inicial após o login. Aqui você encontra:

### Indicadores Principais

1. **Vendas Hoje**: Total vendido no dia atual
2. **Vendas do Mês**: Acumulado do mês
3. **Total de Produtos**: Quantidade de produtos cadastrados
4. **Estoque Baixo**: Produtos que atingiram o estoque mínimo

### Gráficos

- **Vendas dos Últimos 7 Dias**: Visualização das vendas diárias
- **Produtos Mais Vendidos**: Top 5 produtos do mês

### Últimas Vendas

Lista das 10 últimas vendas realizadas, com acesso rápido aos detalhes.

---

## PDV - Ponto de Venda

O PDV é o coração do sistema para vendas rápidas.

### Como Realizar uma Venda

1. **Acesse**: Menu lateral → "PDV - Vendas"

2. **Buscar Produtos**:
   - Digite o nome ou código do produto
   - Clique no produto desejado para adicionar ao carrinho

3. **Gerenciar Carrinho**:
   - Use os botões `+` e `-` para ajustar quantidade
   - Clique no `X` para remover um item
   - Informe desconto se necessário

4. **Selecionar Cliente** (Opcional):
   - Escolha um cliente cadastrado
   - Ou deixe em branco para venda sem cadastro

5. **Forma de Pagamento**:
   - Dinheiro
   - Cartão
   - M-Pesa
   - E-Mola

6. **Finalizar**:
   - Clique em "Finalizar Venda"
   - Imprima o recibo se necessário

### Atalhos no PDV

- **Enter**: Buscar produto
- **ESC**: Limpar busca
- **F2**: Focar no campo de busca

---

## Gestão de Produtos

### Cadastrar Novo Produto

1. **Acesse**: Produtos → "Novo Produto"

2. **Informações Obrigatórias**:
   - Código (único)
   - Nome do produto
   - Preço de custo
   - Preço de venda

3. **Informações Opcionais**:
   - Descrição
   - Categoria
   - Fornecedor
   - Estoque inicial
   - Estoque mínimo
   - Unidade de medida

4. **Clique em "Cadastrar"**

### Editar Produto

1. Acesse "Produtos" → Clique no ícone de lápis
2. Faça as alterações necessárias
3. Clique em "Atualizar"

### Categorias

Organize seus produtos em categorias:

1. Acesse "Produtos" → "Categorias"
2. Clique em "Nova Categoria"
3. Informe nome e descrição
4. Salve

**Categorias sugeridas**:
- Alimentação
- Bebidas
- Higiene e Limpeza
- Eletrônicos
- Vestuário

---

## Controle de Estoque

### Consultar Estoque

1. **Acesse**: Menu → "Estoque"
2. Visualize todos os produtos com seus níveis de estoque
3. Use o filtro "Estoque Baixo" para ver produtos que precisam de reposição

### Ajustar Estoque

1. Na lista de estoque, clique no ícone de caixa
2. Selecione o tipo de movimento:
   - **Entrada**: Recebimento de mercadoria
   - **Saída**: Perda, devolução, etc.
   - **Ajuste**: Correção de estoque

3. Informe a quantidade
4. Descreva o motivo
5. Confirme

### Histórico de Movimentos

1. Acesse "Estoque" → "Movimentos"
2. Visualize todo o histórico
3. Filtre por produto ou tipo de movimento

---

## Gestão de Clientes

### Cadastrar Cliente

1. **Acesse**: Menu → "Clientes" → "Novo Cliente"

2. **Informações**:
   - Nome (obrigatório)
   - CPF/NUIT
   - Email
   - Telefone
   - Endereço
   - Cidade
   - Observações

3. **Clique em "Cadastrar"**

### Benefícios de Cadastrar Clientes

- Histórico de compras
- Relatórios de clientes
- Campanhas de marketing
- Atendimento personalizado

---

## Gestão de Fornecedores

### Cadastrar Fornecedor

1. **Acesse**: Menu → "Fornecedores" → "Novo Fornecedor"

2. **Informações**:
   - Nome da empresa
   - NUIT
   - Email
   - Telefone
   - Endereço
   - Cidade
   - Observações

3. **Clique em "Cadastrar"**

### Vincular Produtos a Fornecedores

Ao cadastrar/editar um produto, selecione o fornecedor na lista.

---

## Controle de Caixa

### Abrir Caixa

**IMPORTANTE**: Abra o caixa ANTES de começar as vendas!

1. **Acesse**: Menu → "Caixa"
2. Clique em "Abrir Caixa"
3. Informe o saldo inicial (dinheiro no caixa)
4. Confirme

### Durante o Dia

- Todas as vendas são registradas automaticamente
- Você pode adicionar movimentos manuais:
  - Sangria (retirada de dinheiro)
  - Reforço (entrada de dinheiro)

### Fechar Caixa

**No final do dia**:

1. Acesse "Caixa"
2. Revise as movimentações
3. Verifique o saldo final
4. Adicione observações se necessário
5. Clique em "Fechar Caixa"

### Relatório do Caixa

O sistema mostra automaticamente:
- Total de entradas
- Total de saídas
- Vendas por forma de pagamento
- Saldo final

---

## Relatórios

### Relatório de Vendas

1. **Acesse**: Menu → "Relatórios" → "Vendas"

2. **Filtros**:
   - Data inicial
   - Data final

3. **Informações**:
   - Total de vendas
   - Valor total
   - Ticket médio
   - Vendas por forma de pagamento

4. **Exportar**: Clique em "Exportar PDF"

### Produtos Mais Vendidos

1. **Acesse**: "Relatórios" → "Produtos"
2. Selecione o período
3. Visualize o ranking

### Relatório de Clientes

1. **Acesse**: "Relatórios" → "Clientes"
2. Veja quem são seus melhores clientes
3. Total de compras por cliente

---

## Dicas e Boas Práticas

### Rotina Diária Recomendada

**Início do Dia**:
1. Abrir o caixa
2. Verificar estoque baixo
3. Revisar pendências

**Durante o Dia**:
1. Realizar vendas pelo PDV
2. Cadastrar novos clientes
3. Ajustar estoque quando necessário

**Fim do Dia**:
1. Conferir vendas
2. Fechar o caixa
3. Gerar relatório do dia

### Segurança

1. **Senhas**:
   - Use senhas fortes
   - Altere periodicamente
   - Não compartilhe

2. **Backup**:
   - Faça backup diário do banco de dados
   - Armazene em local seguro

3. **Acessos**:
   - Dê acesso apenas ao necessário
   - Vendedores: apenas PDV
   - Gerentes: PDV + Relatórios
   - Admin: acesso total

### Manutenção

**Semanal**:
- Verificar produtos com estoque baixo
- Revisar produtos sem movimentação
- Analisar relatórios de vendas

**Mensal**:
- Fazer backup completo
- Revisar cadastros de clientes/fornecedores
- Analisar rentabilidade

### Dicas de Venda

1. **Cadastre seus clientes**: Ajuda nas campanhas de marketing
2. **Use códigos de barras**: Agiliza o PDV
3. **Mantenha estoque atualizado**: Evita vender sem produto
4. **Defina estoque mínimo**: Receba alertas automáticos
5. **Revise preços regularmente**: Mantenha competitividade

---

## Suporte

### Problemas Comuns

**Não consigo fazer login**:
- Verifique email e senha
- Confirme se o usuário está ativo

**Produto não aparece no PDV**:
- Verifique se está ativo
- Confirme o nome/código

**Erro ao finalizar venda**:
- Verifique se há caixa aberto
- Confirme estoque dos produtos

### Contato

Para suporte técnico, entre em contato através do email configurado no sistema.

---

**Sistema desenvolvido para Moçambique** 🇲🇿

*Versão 1.0 - Janeiro 2026*
