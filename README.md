# TODO API - FastAPI Backend

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=for-the-badge&logo=mongodb&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens)

> **Backend API RESTful para aplicação de gerenciamento de tarefas (TODOs) construído com FastAPI, autenticação JWT e MongoDB.**

Este projeto é o backend do curso **"Python Desenvolvedor 2025 - Do Zero ao Avançado"** e será integrado com um frontend React.js.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Fluxo de Dados](#-fluxo-de-dados)
- [Endpoints da API](#-endpoints-da-api)
- [Autenticação e Autorização](#-autenticação-e-autorização)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Integração Frontend](#-integração-frontend)
- [Contribuição](#-contribuição)

## 🎯 Visão Geral

Esta API permite aos usuários:

- **Criar conta** e fazer **login** com autenticação segura
- **Gerenciar tarefas pessoais** (CRUD completo)
- **Autenticação JWT** com tokens de acesso e refresh
- **Autorização baseada em propriedade** - usuários só acessam suas próprias tarefas
- **Documentação automática** com Swagger UI
- **Validação robusta** de dados com Pydantic

## ✨ Funcionalidades

### 🔐 Autenticação
- [x] Registro de usuários com validação
- [x] Login com JWT (Access + Refresh Tokens)
- [x] Proteção de rotas com middleware de autenticação
- [x] Validação de tokens e controle de expiração

### 📝 Gerenciamento de TODOs
- [x] Criar tarefas com título, descrição e status
- [x] Listar todas as tarefas do usuário autenticado
- [x] Visualizar detalhes de uma tarefa específica
- [x] Atualizar tarefas (título, descrição, status)
- [x] Deletar tarefas
- [x] Autorização baseada em propriedade (ownership)

### 🛡️ Segurança
- [x] Hash de senhas com bcrypt
- [x] Tokens JWT com expiração configurável
- [x] CORS configurado para frontend React
- [x] Validação rigorosa de entrada de dados

## 🏗️ Arquitetura

### Padrão de Arquitetura: **Layered Architecture**

```
┌─────────────────┐
│   🌐 API Layer   │  ← FastAPI Routes & Dependencies
├─────────────────┤
│ 📋 Service Layer │  ← Business Logic & Data Processing
├─────────────────┤
│  💾 Model Layer  │  ← Database Models & Schemas
├─────────────────┤
│   🗄️ Data Layer   │  ← MongoDB with Beanie ODM
└─────────────────┘
```

### Componentes Principais:

- **🎯 Handlers**: Controladores da API (rotas e validações)
- **⚙️ Services**: Lógica de negócio e processamento de dados
- **📊 Models**: Modelos de dados e schemas Pydantic
- **🔐 Auth**: Sistema de autenticação JWT
- **⚡ Dependencies**: Injeção de dependências FastAPI
- **🛠️ Core**: Configurações e utilitários centrais

## 🚀 Tecnologias

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| **Python** | 3.8+ | Linguagem principal |
| **FastAPI** | Latest | Framework web moderno e rápido |
| **MongoDB** | Latest | Banco de dados NoSQL |
| **Beanie** | Latest | ODM assíncrono para MongoDB |
| **Pydantic** | V2 | Validação de dados e serialização |
| **JWT** | - | Autenticação via JSON Web Tokens |
| **Bcrypt** | - | Hash seguro de senhas |
| **Python-Decouple** | - | Gerenciamento de variáveis de ambiente |

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- MongoDB (local ou Atlas)
- Git

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/fastapi-todo-api.git
cd fastapi-todo-api
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install fastapi uvicorn[standard] motor beanie pydantic[email] python-jose[cryptography] passlib[bcrypt] python-multipart python-decouple
```

4. **Configure as variáveis de ambiente**
```bash
# Crie um arquivo .env na raiz do projeto
touch .env
```

## ⚙️ Configuração

### Arquivo `.env`

```env
# Configurações do Projeto
PROJECT_NAME=TODO-AUTH-API

# JWT Configuration
JWT_SECRET_KEY=sua-chave-secreta-super-segura-aqui
JWT_REFRESH_SECRET_KEY=sua-chave-refresh-super-segura-aqui
ALGORITHM=HS256

# Database
MONGO_CONNECTION_STRING=mongodb://localhost:27017/todo_db
# ou para MongoDB Atlas:
# MONGO_CONNECTION_STRING=mongodb+srv://usuario:senha@cluster.mongodb.net/todo_db

# CORS Origins (para desenvolvimento)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8080"]
```

### ⚠️ Segurança

- **Nunca** commite o arquivo `.env`
- Use chaves JWT fortes (recomendado 256+ caracteres)
- Em produção, use variáveis de ambiente do servidor

## 🎮 Uso

### Iniciar o servidor

```bash
# Modo desenvolvimento
uvicorn app.app:app --reload --host 0.0.0.0 --port 8000

# Modo produção
uvicorn app.app:app --host 0.0.0.0 --port 8000
```

### Acessar a documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/api/v1/openapi.json

## 🔄 Fluxo de Dados

### 1. 🔐 Fluxo de Autenticação

```mermaid
sequenceDiagram
    participant C as Cliente
    participant API as FastAPI
    participant Auth as AuthService
    participant DB as MongoDB
    
    C->>API: POST /auth/register {email, password}
    API->>Auth: create_user()
    Auth->>DB: Salva usuário (senha hasheada)
    DB-->>Auth: user_id
    Auth-->>API: UserDetail
    API-->>C: 201 Created
    
    C->>API: POST /auth/login {email, password}
    API->>Auth: authenticate_user()
    Auth->>DB: Busca usuário por email
    DB-->>Auth: User data
    Auth->>Auth: Verifica senha (bcrypt)
    Auth->>Auth: Gera JWT tokens
    Auth-->>API: {access_token, refresh_token}
    API-->>C: 200 OK + Tokens
```

### 2. 📝 Fluxo de Gerenciamento de TODOs

```mermaid
sequenceDiagram
    participant C as Cliente
    participant API as FastAPI
    participant Deps as Dependencies
    participant Service as TodoService
    participant DB as MongoDB
    
    C->>API: GET /todo/ + Bearer Token
    API->>Deps: get_current_user(token)
    Deps->>Deps: Valida JWT
    Deps->>DB: Busca usuário por ID
    DB-->>Deps: User object
    Deps-->>API: current_user
    API->>Service: list_todos(user)
    Service->>DB: Todo.find(owner.id == user.id)
    DB-->>Service: Lista de TODOs
    Service-->>API: List[Todo]
    API-->>C: 200 OK + TODOs
```

### 3. 🛡️ Fluxo de Autorização

```mermaid
flowchart TD
    A[Requisição com Token] --> B{Token Válido?}
    B -->|Não| C[401 Unauthorized]
    B -->|Sim| D[Extrai user_id do token]
    D --> E[Busca User no banco]
    E --> F{User existe?}
    F -->|Não| G[404 User Not Found]
    F -->|Sim| H[Executa operação]
    H --> I{Recurso pertence ao User?}
    I -->|Não| J[404 Not Found]
    I -->|Sim| K[200 OK + Dados]
```

## 📚 Endpoints da API

### 🔐 Autenticação (`/api/v1/auth`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `POST` | `/register` | Criar nova conta | ❌ |
| `POST` | `/login` | Fazer login | ❌ |
| `POST` | `/refresh` | Renovar access token | ✅ |

### 👤 Usuários (`/api/v1/users`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/me` | Dados do usuário atual | ✅ |
| `GET` | `/test` | Teste de conectividade | ❌ |

### 📝 TODOs (`/api/v1/todo`)

| Método | Endpoint | Descrição | Auth |
|--------|----------|-----------|------|
| `GET` | `/` | Listar TODOs do usuário | ✅ |
| `POST` | `/create` | Criar novo TODO | ✅ |
| `GET` | `/{todo_id}` | Detalhes de um TODO | ✅ |
| `PATCH` | `/{todo_id}` | Atualizar TODO | ✅ |
| `DELETE` | `/{todo_id}` | Deletar TODO | ✅ |

### 📋 Exemplos de Uso

#### Registrar usuário
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao123",
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=joao@example.com&password=senha123"
```

#### Criar TODO
```bash
curl -X POST "http://localhost:8000/api/v1/todo/create" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar FastAPI",
    "description": "Completar o curso de FastAPI",
    "status": false
  }'
```

#### Atualizar TODO
```bash
curl -X PATCH "http://localhost:8000/api/v1/todo/123e4567-e89b-12d3-a456-426614174000" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "status": true
  }'
```

## 🔐 Autenticação e Autorização

### Sistema de Autenticação

1. **Registro**: Senha é hasheada com bcrypt antes do armazenamento
2. **Login**: Credenciais são validadas e tokens JWT são gerados
3. **Access Token**: Expira em 15 minutos (configurável)
4. **Refresh Token**: Expira em 7 dias (configurável)

### Sistema de Autorização

- **Baseado em Propriedade**: Usuários só acessam recursos que criaram
- **Filtros Automáticos**: Consultas incluem `owner.id == user.id`
- **Validação por Endpoint**: Cada rota protegida valida ownership

### Headers de Autenticação

```http
Authorization: Bearer <access_token>
```

### Estrutura do Token JWT

```json
{
  "sub": "user_id_uuid",
  "iat": 1640995200,
  "exp": 1640996100
}
```

## 📁 Estrutura do Projeto

```
app/
├── 📱 app.py                    # Aplicação principal FastAPI
├── 🔧 core/
│   ├── config.py               # Configurações globais
│   └── security.py             # Utilitários de segurança
├── 🗄️ models/
│   ├── user_model.py           # Modelo de usuário
│   └── todo_model.py           # Modelo de TODO
├── 📋 schemas/
│   ├── user_schema.py          # Schemas de usuário
│   ├── todo_schema.py          # Schemas de TODO
│   └── auth_schema.py          # Schemas de autenticação
├── ⚙️ services/
│   ├── user_service.py         # Lógica de negócio - usuários
│   └── todo_service.py         # Lógica de negócio - TODOs
├── 🌐 api/
│   ├── api_v1/
│   │   ├── router.py          # Router principal v1
│   │   └── handlers/
│   │       ├── user.py        # Endpoints de usuário
│   │       └── todo.py        # Endpoints de TODO
│   ├── auth/
│   │   └── jwt.py             # Endpoints de autenticação
│   └── dependencies/
│       └── user_deps.py       # Dependências de usuário
└── 📄 README.md               # Este arquivo
```

### 🧩 Responsabilidades por Camada

| Camada | Responsabilidade |
|--------|------------------|
| **🌐 Handlers** | Validação de entrada, serialização de resposta, códigos HTTP |
| **⚙️ Services** | Lógica de negócio, processamento de dados, orquestração |
| **🗄️ Models** | Estrutura de dados, validações, relacionamentos |
| **📋 Schemas** | Contratos de API, validação Pydantic, documentação |
| **🔐 Auth** | Autenticação JWT, autorização, middleware de segurança |
| **🔧 Core** | Configurações, utilitários globais, constantes |

## 🔗 Integração Frontend

### Configuração para React.js

1. **CORS**: Já configurado para `localhost:3000`
2. **Base URL**: `http://localhost:8000/api/v1`
3. **Autenticação**: Bearer Token no header

### Exemplo de Cliente React

```typescript
// api.ts
const API_BASE = 'http://localhost:8000/api/v1';

export const authAPI = {
  login: async (email: string, password: string) => {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `username=${email}&password=${password}`
    });
    return response.json();
  }
};

export const todoAPI = {
  list: async (token: string) => {
    const response = await fetch(`${API_BASE}/todo/`, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    return response.json();
  },
  
  create: async (token: string, todo: CreateTodoDto) => {
    const response = await fetch(`${API_BASE}/todo/create`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(todo)
    });
    return response.json();
  }
};
```

### Hooks React Sugeridos

```typescript
// useAuth.ts
export const useAuth = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));
  
  const login = async (email: string, password: string) => {
    const { access_token } = await authAPI.login(email, password);
    setToken(access_token);
    localStorage.setItem('token', access_token);
  };
  
  return { token, login };
};

// useTodos.ts
export const useTodos = (token: string) => {
  const [todos, setTodos] = useState([]);
  
  const fetchTodos = async () => {
    const data = await todoAPI.list(token);
    setTodos(data);
  };
  
  return { todos, fetchTodos };
};
```

## 🧪 Testing

### Testes Manuais

1. **Swagger UI**: http://localhost:8000/docs
2. **Curl**: Exemplos fornecidos acima
3. **Postman**: Importe a collection OpenAPI

### Cenários de Teste

- [ ] Registro de usuário com dados válidos
- [ ] Login com credenciais corretas  
- [ ] Acesso negado sem token
- [ ] CRUD completo de TODOs
- [ ] Autorização (usuário A não vê TODOs do usuário B)
- [ ] Expiração de token

## 🚀 Deploy

### Variáveis de Ambiente (Produção)

```env
PROJECT_NAME=TODO-API-PROD
JWT_SECRET_KEY=chave-ultra-secreta-produção-256-chars
JWT_REFRESH_SECRET_KEY=chave-refresh-ultra-secreta-produção-256-chars
MONGO_CONNECTION_STRING=mongodb+srv://user:pass@cluster.mongodb.net/todo_prod
BACKEND_CORS_ORIGINS=["https://meuapp.com","https://www.meuapp.com"]
```

### Docker (Opcional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: Amazing Feature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Curso: Python Desenvolvedor 2025 - Do Zero ao Avançado**
- 📧 Email: [seu-email@example.com]
- 🐱 GitHub: [@seu-usuario]

---

⭐ **Se este projeto foi útil, deixe uma estrela!** ⭐
