# Cadete Funcional (SCF)

Sistema de Atendimento Médico para o Cadete - Desenvolvido por DTSIC AMAN

## 📁 Estrutura do Projeto

Este projeto segue as melhores práticas de desenvolvimento Django com uma estrutura organizada:

```
cadete_funcional/
├── cadete_funcional/          # ⚙️ Configurações Django
│   ├── settings/             # Configurações divididas por ambiente
│   │   ├── base.py          # Configurações base
│   │   ├── dev.py           # Desenvolvimento
│   │   └── prod.py          # Produção
│   ├── urls.py              # URLs principais
│   ├── wsgi.py              # WSGI
│   └── asgi.py              # ASGI
├── core/                     # 🏥 App principal do sistema
│   ├── templates/core/      # Templates específicos do app
│   ├── migrations/          # Migrações do banco
│   └── ...
├── integracao/               # 🔗 App de integração de dados
├── templates/                # 🎨 Templates globais
├── config/                   # ⚙️ Arquivos de configuração
│   ├── .env                 # Variáveis de ambiente
│   ├── .env.example         # Exemplo de configuração
│   ├── Dockerfile           # Configuração Docker
│   └── gunicorn.conf.py     # Configuração Gunicorn
├── docs/                     # 📚 Documentação
├── scripts/                  # 🔧 Scripts utilitários
├── docker/                   # 🐳 Configurações Docker
├── manage.py                 # 🏃 Script de gerenciamento Django
├── requirements.txt          # 📦 Dependências Python
├── .gitignore               # 🚫 Arquivos ignorados pelo Git
└── README.md                # 📖 Este arquivo
```

## 🎯 Melhorias Implementadas

### ✅ Estrutura Organizada
- **Separação clara** entre configurações, apps e templates
- **Configurações por ambiente** (desenvolvimento/produção)
- **Documentação centralizada** na pasta `docs/`
- **Scripts utilitários** organizados na pasta `scripts/`

### ✅ Configurações de Ambiente
- Arquivos `.env` organizados na pasta `config/`
- Configurações específicas por ambiente
- Variáveis de ambiente bem documentadas

### ✅ Templates Estruturados
- Templates globais em `templates/`
- Templates específicos por app em `app/templates/app/`
- Separação clara entre layouts globais e específicos

### ✅ Documentação Completa
- README atualizado com estrutura do projeto
- Documentação de instalação e deployment
- Guias de configuração e uso

## 🚀 Instalação e Execução

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose (opcional)
- PostgreSQL (produção) ou SQLite (desenvolvimento)

### Instalação Local

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd cadete_funcional
   ```

2. **Configure o ambiente virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # ou
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```bash
   cp config/.env.example config/.env
   # Edite o config/.env com suas configurações
   ```

5. **Execute as migrações:**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

### Execução com Docker

```bash
docker-compose up -d
```

## 📋 Funcionalidades

- ✅ Dashboard com estatísticas em tempo real
- ✅ Gerenciamento de Cadetes
- ✅ Registro de Atendimentos Médicos
- ✅ API REST para integração
- ✅ Interface administrativa moderna (Jazzmin)
- ✅ Sistema de autenticação
- ✅ Relatórios e estatísticas

## 🛠️ Tecnologias Utilizadas

- **Backend:** Django 5.0+
- **Banco de Dados:** PostgreSQL (prod) / SQLite (dev)
- **API:** Django REST Framework
- **Interface Admin:** Django Jazzmin
- **Frontend:** Bootstrap 5, Font Awesome
- **Containerização:** Docker & Docker Compose
- **Deploy:** Gunicorn + Nginx

## 📚 Documentação

- [Instalação e Deploy](docs/INSTALACAO_DEPLOYMENT.md)
- [Configuração do Ambiente](docs/SETUP_PRONTO.md)
- [Setup Rápido](docs/SETUP_RÁPIDO.md)
- [Atendimento ao Usuário](docs/atendimento_usuario.md)

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Desenvolvedores

**DTSIC AMAN** - Desenvolvimento e manutenção

---

**Cadete Funcional (SCF)** - Sistema de Atendimento Médico para o Cadete