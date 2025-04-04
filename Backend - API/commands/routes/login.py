from fastapi import APIRouter, HTTPException
from commands.database import usuarios_collection,personagens_collection
from commands.models.user_model import Usuario
from commands.func_senhas import hash_senha, verificar_senha
from bson import ObjectId

router = APIRouter()

# Endpoint de Registro
@router.post("/register")
def register(usuario: Usuario) -> dict:
    """
    Registra um novo usuário no banco de dados, aplicando hash e salt na senha,
    e cria um personagem inicial associado ao usuário.

    Parâmetros:
        usuario (Usuario): Objeto contendo username e password.

    Retorna:
        dict: Mensagem indicando sucesso ou erro.

    Erros:
        - 400: Se o nome de usuário já existir.
        - 400: Se o nome de usuário for maior que 14 caracteres.
        - 400: Se a senha não tiver entre 6 e 14 caracteres.

    Exemplo de Uso:
        POST /register
        {
            "username": "guerreiro123",
            "password": "senha_secreta"
        }
    """

    if len(usuario.username) > 14:
        raise HTTPException(status_code=400, detail="O nome de usuário não pode ter mais que 14 caracteres!")

    if len(usuario.password) > 14 or len(usuario.password) < 6:
        raise HTTPException(status_code=400, detail="A senha precisa ter entre 6 e 14 caracteres!")

    if usuarios_collection.find_one({"username": usuario.username}):
        raise HTTPException(status_code=400, detail="Usuário já existe")

    salt, senha_hash = hash_senha(usuario.password)
    resultado = usuarios_collection.insert_one({
        "username": usuario.username,
        "salt": salt,
        "password": senha_hash
    })
    user_id = resultado.inserted_id

    personagens_collection.insert_one({
        "user_id": ObjectId(user_id),
        "personagens": []
    })

    return {"message": "Usuário criado com sucesso"}

# Endpoint de Login
@router.post("/login")
def login(usuario: Usuario) -> dict:
    """
    Realiza login verificando username e senha com hash e salt.

    Parâmetros:
        usuario (Usuario): Objeto contendo username e password.

    Retorna:
        dict: Mensagem indicando sucesso ou erro.

    Erros:
        - 401: Se o usuário não for encontrado.
        - 401: Se a senha estiver incorreta.

    Exemplo de Uso:
        POST /login
        {
            "username": "guerreiro123",
            "password": "senha_secreta"
        }
    """
    user = usuarios_collection.find_one({"username": usuario.username})

    if not user or not verificar_senha(usuario.password, user["salt"], user["password"]):
        raise HTTPException(status_code=401, detail="Usuário ou Senha inválido!")

    return {"message": "Login bem-sucedido"}

