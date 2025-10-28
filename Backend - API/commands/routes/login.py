"""
MidianText RPG - Rotas de Autenticação
=======================================

Este módulo implementa os endpoints de autenticação do sistema, incluindo
registro de usuários e login com geração de tokens JWT.

Endpoints:
    POST /register - Registro de novos usuários
    POST /login    - Autenticação e geração de token

Segurança:
    - Senhas hasheadas com PBKDF2-HMAC-SHA256 + salt único
    - Tokens JWT com expiração de 2 horas
    - Validações de comprimento de username/password
    - Verificação de unicidade de username

Fluxo de Registro:
    1. Cliente envia username + password
    2. Validações de comprimento (username ≤ 14, password 6-14)
    3. Verificação de username duplicado
    4. Geração de salt + hash da senha
    5. Criação de documento no Firebase (usuarios)
    6. Inicialização de lista de personagens vazia
    7. Retorno de confirmação

Fluxo de Login:
    1. Cliente envia username + password
    2. Busca usuário no Firebase
    3. Verificação de senha com salt armazenado
    4. Geração de token JWT (válido por 2 horas)
    5. Retorno de token + confirmação

Estrutura de Dados:
    Firebase - Collection 'usuarios':
        {
            "username": str,       # Nome de usuário único
            "salt": str,           # Salt hexadecimal (16 bytes)
            "password": str        # Hash hexadecimal da senha
        }
    
    Firebase - Collection 'personagens':
        {
            "user_id": str,        # ID do documento de usuário
            "personagens": []      # Lista de personagens (inicialmente vazia)
        }

HTTP Status Codes:
    - 200: Operação bem-sucedida
    - 400: Validação falhou (username/password inválidos ou duplicados)
    - 401: Credenciais incorretas (login falhou)

Dependencies:
    - FastAPI: Framework web
    - Firebase Firestore: Armazenamento de usuários
    - func_senhas: Hashing de senhas
    - key_manager: Geração de tokens JWT
    - user_model: Validação de dados de entrada

"""

from fastapi import APIRouter, HTTPException
from commands.database import usuarios_collection, personagens_collection
from commands.models.user_model import Usuario
from commands.func_senhas import hash_senha, verificar_senha
from commands.key_manager import generate_key

router = APIRouter()


# Endpoint de Registro
@router.post("/register")
def register(usuario: Usuario) -> dict:
    """
    Registra um novo usuário no sistema com senha hasheada e personagem inicial.
    
    Este endpoint cria um novo usuário no Firebase com credenciais seguras,
    gerando salt único e hash PBKDF2 da senha. Também inicializa a estrutura
    de personagens associada ao usuário.
    
    Args:
        usuario (Usuario): Modelo Pydantic contendo:
            - username (str): Nome de usuário (máx 14 caracteres)
            - password (str): Senha em texto plano (6-14 caracteres)
    
    Returns:
        dict: Resposta de sucesso
            {
                "message": "Usuário criado com sucesso"
            }
    
    Raises:
        HTTPException 400: 
            - Username > 14 caracteres
            - Password < 6 ou > 14 caracteres
            - Username já existe no banco
    
    Example:
        >>> # Requisição HTTP
        >>> POST /register
        >>> {
        ...     "username": "guerreiro123",
        ...     "password": "senha_secreta"
        ... }
        >>> 
        >>> # Resposta de sucesso
        >>> {
        ...     "message": "Usuário criado com sucesso"
        ... }
        >>> 
        >>> # Resposta de erro (username duplicado)
        >>> {
        ...     "detail": "Usuário já existe"
        ... }
    
    Process:
        1. Valida comprimento de username (≤ 14 chars)
        2. Valida comprimento de password (6-14 chars)
        3. Verifica se username já existe no Firestore
        4. Gera salt aleatório (16 bytes) + hash PBKDF2
        5. Cria documento em 'usuarios' collection
        6. Cria documento em 'personagens' collection (lista vazia)
        7. Retorna confirmação
    
    Security Notes:
        - Senha NUNCA armazenada em texto plano
        - Salt único por usuário (previne rainbow tables)
        - Hash PBKDF2 com 100.000 iterações (dificulta brute-force)
        - Validações de entrada previnem ataques de buffer overflow
    
    Database Changes:
        - Collection 'usuarios': +1 documento
        - Collection 'personagens': +1 documento
        - Ambos com mesmo ID de referência
    
    Frontend Usage:
        ```python
        response = requests.post(
            "http://localhost:8000/register",
            json={"username": "player1", "password": "pass123"}
        )
        if response.status_code == 200:
            print("Registro bem-sucedido!")
        ```
    """
    # Validação de comprimento de username
    if len(usuario.username) > 14:
        raise HTTPException(
            status_code=400,
            detail="O nome de usuário não pode ter mais que 14 caracteres!"
        )

    # Validação de comprimento de senha
    if len(usuario.password) > 14 or len(usuario.password) < 6:
        raise HTTPException(
            status_code=400,
            detail="A senha precisa ter entre 6 e 14 caracteres!"
        )

    # Verifica se o usuário já existe
    query = usuarios_collection.where("username", "==", usuario.username).get()
    if len(query) > 0:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Gera salt e hash da senha
    salt, senha_hash = hash_senha(usuario.password)
    
    # Adiciona usuário ao Firestore
    user_ref = usuarios_collection.add({
        "username": usuario.username,
        "salt": salt,
        "password": senha_hash
    })
    user_id = user_ref[1].id  # O ID do documento criado

    # Cria documento de personagens associado ao usuário
    # Inicializa com lista vazia (personagens criados posteriormente)
    personagens_collection.document(user_id).set({
        "user_id": user_id,
        "personagens": []
    })

    return {"message": "Usuário criado com sucesso"}


# Endpoint de Login
@router.post("/login")
def login(usuario: Usuario) -> dict:
    """
    Autentica usuário e retorna token JWT para sessão.
    
    Verifica credenciais comparando senha fornecida com hash armazenado
    usando salt do usuário. Em caso de sucesso, gera token JWT válido
    por 2 horas para autenticação stateless.
    
    Args:
        usuario (Usuario): Modelo Pydantic contendo:
            - username (str): Nome de usuário
            - password (str): Senha em texto plano
    
    Returns:
        dict: Resposta de sucesso com token JWT
            {
                "message": "Login bem-sucedido",
                "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
    
    Raises:
        HTTPException 401:
            - Usuário não encontrado no banco
            - Senha incorreta
    
    Example:
        >>> # Requisição HTTP
        >>> POST /login
        >>> {
        ...     "username": "guerreiro123",
        ...     "password": "senha_secreta"
        ... }
        >>> 
        >>> # Resposta de sucesso
        >>> {
        ...     "message": "Login bem-sucedido",
        ...     "key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYWJjMTIzIn0.xyz"
        ... }
        >>> 
        >>> # Resposta de erro
        >>> {
        ...     "detail": "Usuário ou Senha inválido!"
        ... }
    
    Process:
        1. Busca usuário no Firestore por username
        2. Verifica se usuário existe
        3. Extrai salt e password_hash armazenados
        4. Aplica PBKDF2 na senha fornecida com salt armazenado
        5. Compara hash gerado com hash armazenado
        6. Gera token JWT com user_id (válido 2 horas)
        7. Retorna token para cliente
    
    Security Notes:
        - Mensagem de erro genérica (não revela se user/password está errado)
        - Verificação em tempo constante (previne timing attacks)
        - Token JWT contém apenas user_id (sem dados sensíveis)
        - Token expira em 2 horas (sessão limitada)
    
    Token Usage:
        Cliente deve incluir token em requisições subsequentes:
        ```
        Authorization: Bearer <token>
        ```
    
    Frontend Usage:
        ```python
        response = requests.post(
            "http://localhost:8000/login",
            json={"username": "player1", "password": "pass123"}
        )
        if response.status_code == 200:
            token = response.json()["key"]
            # Armazenar token para requisições futuras
            session["auth_token"] = token
        ```
    
    Authentication Flow:
        1. Login bem-sucedido → Recebe token
        2. Armazena token no cliente (memória/sessão)
        3. Inclui token em headers de requisições protegidas
        4. Backend valida token via verify_key()
        5. Token expira → Cliente faz login novamente
    """
    # Busca usuário por username
    query = usuarios_collection.where("username", "==", usuario.username).get()
    if not query:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou Senha inválido!"
        )

    # Extrai dados do primeiro documento encontrado
    user_doc = query[0]
    user = user_doc.to_dict()
    user_id = user_doc.id

    # Verifica senha com salt armazenado
    if not verificar_senha(usuario.password, user["salt"], user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou Senha inválido!"
        )

    # Gera token JWT com user_id (válido por 2 horas)
    temp_key = generate_key(user_id)

    return {"message": "Login bem-sucedido", "key": temp_key}
