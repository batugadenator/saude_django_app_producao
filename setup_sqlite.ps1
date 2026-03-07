# Script para setup rápido com SQLite (SOLUÇÃO 2)
# Execute este script no PowerShell

Write-Host "`n=== SETUP DJANGO COM SQLITE ===" -ForegroundColor Green

# Passo 1: Criar .env
Write-Host "`n[1/5] Criando arquivo .env..." -ForegroundColor Cyan
@"
DEBUG=True
SECRET_KEY=dev-secret-key-insecure-only-for-local-dev
ALLOWED_HOSTS=localhost,127.0.0.1,*
DJANGO_SETTINGS_MODULE=saude_project.settings.dev
"@ | Out-File .env -Encoding UTF8
Write-Host "✓ Arquivo .env criado" -ForegroundColor Green

# Passo 2: Instalar dependências
Write-Host "`n[2/5] Instalando dependências..." -ForegroundColor Cyan
pip install -r requirements.txt 2>&1 | Select-Object -Last 3
Write-Host "✓ Dependências instaladas" -ForegroundColor Green

# Passo 3: Criar migrations
Write-Host "`n[3/5] Criando migrations..." -ForegroundColor Cyan
python manage.py makemigrations
Write-Host "✓ Migrations criadas" -ForegroundColor Green

# Passo 4: Aplicar migrations
Write-Host "`n[4/5] Aplicando migrations..." -ForegroundColor Cyan
python manage.py migrate
Write-Host "✓ Migrations aplicadas" -ForegroundColor Green

# Passo 5: Criar superuser
Write-Host "`n[5/5] Criando superuser (admin)..." -ForegroundColor Cyan
Write-Host "User: admin" -ForegroundColor Yellow
Write-Host "Password: admin123" -ForegroundColor Yellow
Write-Host "Email: admin@example.com" -ForegroundColor Yellow

echo "admin
admin@example.com
admin123
admin123" | python manage.py createsuperuser --noinput

Write-Host "`n✓ Superuser criado!" -ForegroundColor Green

# Sucesso
Write-Host "`n╔════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     ✓ SETUP CONCLUÍDO COM SUCESSO!                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`nPróximos passos:`n" -ForegroundColor Cyan
Write-Host "1. Rodar servidor:" -ForegroundColor Yellow
Write-Host "   python manage.py runserver" -ForegroundColor White

Write-Host "`n2. Acesse no navegador:" -ForegroundColor Yellow
Write-Host "   http://localhost:8000/admin" -ForegroundColor White

Write-Host "`n3. Faça login com:" -ForegroundColor Yellow
Write-Host "   Username: admin" -ForegroundColor White
Write-Host "   Password: admin123" -ForegroundColor White

Write-Host "`n4. Importar dados da planilha (opcional):" -ForegroundColor Yellow
Write-Host "   python manage.py import_planilha --arquivo projeto_saude.xlsm" -ForegroundColor White

Write-Host "`n"
