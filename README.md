# MidianText-RPG_API

Esta aplicação é uma **API backend** construída com **FastAPI** que gerencia o registro de usuários, login, criação e listagem de personagens, além de batalhas simples entre jogador e inimigo. Os dados são armazenados em um banco MongoDB, e senhas são protegidas com hash e salt.

## 🚀 Funcionalidades

- ✅ Registro de usuários com verificação de validade e unicidade
- 🔐 Login com autenticação por hash/salt
- 🧙‍♂️ Listagem de personagens de cada usuário
- ⚔️ Sistema simples de batalha entre jogador e inimigo
- 📡 Permite acesso do frontend via CORS

## 📁 Estrutura de Arquivos

```
.
├── database.py         # Conexão com MongoDB
├── func_senhas.py      # Funções de hashing e verificação de senha
├── models.py           # Modelos de dados e lógica de jogo
├── routes.py           # Rotas da API
└── main.py             # Arquivo principal que inicializa o FastAPI
```

## ⚙️ Tecnologias Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [MongoDB](https://www.mongodb.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Python 3.12+](https://www.python.org/)

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/api-rpg-fastapi.git
cd api-rpg-fastapi
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install fastapi uvicorn pymongo python-dotenv
```

### 4. Execute a API

```bash
uvicorn main:app --reload
```

## 🔌 Imports Necessários

Certifique-se de importar os seguintes módulos no seu código:

```python
from fastapi import FastAPI, HTTPException, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
import hashlib, os, random
```

## 📡 Endpoints

### `POST /register`
Cadastra um novo usuário.

### `POST /login`
Realiza login e valida credenciais.

### `GET /personagens/{username}`
Retorna todos os personagens vinculados ao usuário.

### `GET /batalha`
Simula uma batalha entre jogador e inimigo.

## 👤 Autor

Desenvolvido por [Seu Nome ou Equipe].

---

