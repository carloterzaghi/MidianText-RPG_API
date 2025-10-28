"""
MidianText RPG - Servidor API Backend
======================================

Este módulo implementa o servidor FastAPI que gerencia toda a lógica de backend
do jogo MidianText RPG.

O servidor fornece:
- Autenticação e gerenciamento de usuários
- CRUD de personagens
- Sistema de missões
- Integração com Firebase Firestore
- API RESTful com autenticação JWT

Rotas Disponíveis:
    - /register: Registro de novos usuários
    - /login: Autenticação de usuários
    - /personagens/*: Gerenciamento de personagens
    - /missions/*: Sistema de missões

Technology Stack:
    - FastAPI: Framework web assíncrono
    - Firebase Firestore: Banco de dados NoSQL
    - JWT: Autenticação stateless
    - Uvicorn: Servidor ASGI

Port: 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from commands.routes.login import router as login_router
from commands.routes.personagens import router as personagens_router
from commands.routes.missions import router as missions_router


# Inicializa a aplicação FastAPI
app = FastAPI(
    title="MidianText RPG API",
    description="API Backend para o jogo de RPG baseado em texto",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que o frontend (rodando em porta diferente) acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

# Registra os roteadores (blueprints) de cada módulo funcional
app.include_router(login_router, tags=["Autenticação"])
app.include_router(personagens_router, tags=["Personagens"])
app.include_router(missions_router, tags=["Missões"])


@app.get("/", tags=["Sistema"])
async def root():
    """
    Endpoint raiz da API.
    
    Returns:
        dict: Mensagem de boas-vindas e status da API
    
    Example:
        GET /
        Response: {"message": "MidianText RPG API", "status": "online"}
    """
    return {
        "message": "MidianText RPG API",
        "status": "online",
        "version": "1.0.0"
    }


# Executa o servidor quando o módulo é rodado diretamente
if __name__ == "__main__":
    """
    Inicia o servidor Uvicorn com configurações de desenvolvimento.
    
    Configurações:
        - host: "0.0.0.0" - Aceita conexões de qualquer interface de rede
        - port: 8000 - Porta padrão do servidor
        - reload: Auto-reload em desenvolvimento (desabilitar em produção)
    """
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
