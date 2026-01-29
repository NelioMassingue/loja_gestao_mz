# Guia de Deploy em Produção

Este guia cobre a implantação do Sistema de Gestão de Loja em ambiente de produção.

## 📋 Pré-requisitos

- Servidor Linux (Ubuntu 20.04+ recomendado)
- PostgreSQL 12+
- Python 3.8+
- Nginx
- Domínio próprio (opcional)
- Certificado SSL (Let's Encrypt recomendado)

## 🚀 Passos para Deploy

### 1. Preparar o Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx git -y
```

### 2. Configurar PostgreSQL

```bash
# Acessar PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE loja_gestao_mz;
CREATE USER loja_user WITH PASSWORD 'senha_forte_aqui';
GRANT ALL PRIVILEGES ON DATABASE loja_gestao_mz TO loja_user;
\q
```

### 3. Clonar e Configurar Aplicação

```bash
# Criar diretório
sudo mkdir -p /var/www/loja_gestao
cd /var/www/loja_gestao

# Clonar repositório
git clone [seu-repositorio] .

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
nano .env
```

Conteúdo do `.env`:
```env
# Produção
FLASK_ENV=production
SECRET_KEY=gere-uma-chave-muito-forte-e-aleatoria-aqui

# Banco de dados
DATABASE_URL=postgresql://loja_user:senha_forte_aqui@localhost:5432/loja_gestao_mz

# Empresa
EMPRESA_NOME=Nome da Sua Loja
EMPRESA_ENDERECO=Rua X, Maputo, Moçambique
EMPRESA_TELEFONE=+258 XX XXX XXXX
EMPRESA_EMAIL=contato@sualoja.co.mz
EMPRESA_NUIT=000000000
```

### 5. Inicializar Banco de Dados

```bash
source venv/bin/activate
python init_db.py
```

### 6. Configurar Gunicorn

Criar arquivo de serviço:
```bash
sudo nano /etc/systemd/system/loja_gestao.service
```

Conteúdo:
```ini
[Unit]
Description=Sistema de Gestão de Loja
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/loja_gestao
Environment="PATH=/var/www/loja_gestao/venv/bin"
ExecStart=/var/www/loja_gestao/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Ativar serviço:
```bash
sudo systemctl start loja_gestao
sudo systemctl enable loja_gestao
sudo systemctl status loja_gestao
```

### 7. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/loja_gestao
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name seu-dominio.com www.seu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/loja_gestao/static;
        expires 30d;
    }
}
```

Ativar site:
```bash
sudo ln -s /etc/nginx/sites-available/loja_gestao /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 8. Configurar SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática já está configurada
```

### 9. Configurar Firewall

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

### 10. Ajustar Permissões

```bash
sudo chown -R www-data:www-data /var/www/loja_gestao
sudo chmod -R 755 /var/www/loja_gestao
```

## 🔒 Segurança

### Hardening do PostgreSQL

Editar `/etc/postgresql/*/main/pg_hba.conf`:
```
# Permitir apenas localhost
local   all             all                                     peer
host    all             all             127.0.0.1/32            md5
```

Reiniciar PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### Backup Automático

Criar script de backup:
```bash
sudo nano /usr/local/bin/backup_loja.sh
```

Conteúdo:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/loja_gestao"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup do banco
pg_dump -U loja_user loja_gestao_mz > $BACKUP_DIR/db_$DATE.sql

# Backup dos uploads
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /var/www/loja_gestao/static/uploads

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Backup realizado: $DATE"
```

Tornar executável:
```bash
sudo chmod +x /usr/local/bin/backup_loja.sh
```

Agendar backup diário (crontab):
```bash
sudo crontab -e
```

Adicionar:
```
0 2 * * * /usr/local/bin/backup_loja.sh
```

## 📊 Monitoramento

### Logs da Aplicação

Ver logs do Gunicorn:
```bash
sudo journalctl -u loja_gestao -f
```

### Logs do Nginx

```bash
# Acesso
sudo tail -f /var/log/nginx/access.log

# Erros
sudo tail -f /var/log/nginx/error.log
```

### Monitorar Recursos

```bash
# CPU e Memória
htop

# Espaço em disco
df -h

# PostgreSQL
sudo -u postgres psql -c "SELECT * FROM pg_stat_activity;"
```

## 🔄 Atualizações

### Atualizar Aplicação

```bash
cd /var/www/loja_gestao
source venv/bin/activate

# Fazer backup antes
/usr/local/bin/backup_loja.sh

# Atualizar código
git pull

# Atualizar dependências
pip install -r requirements.txt --upgrade

# Reiniciar serviço
sudo systemctl restart loja_gestao
```

## ⚡ Otimizações

### PostgreSQL

Editar `/etc/postgresql/*/main/postgresql.conf`:
```
shared_buffers = 256MB
effective_cache_size = 1GB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
random_page_cost = 1.1
```

Reiniciar:
```bash
sudo systemctl restart postgresql
```

### Nginx

Cache estático:
```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

Compressão:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

## 🆘 Troubleshooting

### Aplicação não inicia

```bash
# Ver logs
sudo journalctl -u loja_gestao -n 50

# Verificar permissões
ls -la /var/www/loja_gestao

# Testar manualmente
cd /var/www/loja_gestao
source venv/bin/activate
python app.py
```

### Erro de banco de dados

```bash
# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Testar conexão
psql -U loja_user -d loja_gestao_mz -h localhost
```

### Nginx não responde

```bash
# Verificar configuração
sudo nginx -t

# Ver logs
sudo tail -f /var/log/nginx/error.log

# Reiniciar
sudo systemctl restart nginx
```

## 📱 Acesso Remoto Seguro

### Via VPN (Recomendado)

Configure uma VPN para acesso remoto seguro ao sistema.

### Via SSH Tunnel

```bash
ssh -L 5000:localhost:5000 usuario@seu-servidor.com
```

Acesse localmente: `http://localhost:5000`

## ✅ Checklist Final

- [ ] PostgreSQL configurado e rodando
- [ ] Aplicação funcionando com Gunicorn
- [ ] Nginx configurado como proxy reverso
- [ ] SSL/HTTPS configurado
- [ ] Firewall ativo e configurado
- [ ] Backups automáticos agendados
- [ ] Logs sendo monitorados
- [ ] Senhas fortes configuradas
- [ ] Usuário admin padrão alterado
- [ ] Dados da empresa configurados
- [ ] Teste completo realizado

## 📞 Suporte

Para problemas específicos do deploy, consulte:
- Documentação do Gunicorn: https://docs.gunicorn.org
- Documentação do Nginx: https://nginx.org/en/docs/
- Documentação do PostgreSQL: https://www.postgresql.org/docs/

---

**Boa sorte com seu deploy!** 🚀
