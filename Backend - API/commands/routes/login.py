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

    # Verifica se o usuário já existe
    query = usuarios_collection.where("username", "==", usuario.username).get()
    if len(query) > 0:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    salt, senha_hash = hash_senha(usuario.password)
    # Adiciona usuário ao Firestore
    user_ref = usuarios_collection.add({
        "username": usuario.username,
        "salt": salt,
        "password": senha_hash
    })
    user_id = user_ref[1].id  # O ID do documento criado

    # Cria documento de personagens associado ao usuário
    personagens_collection.document(user_id).set({
        "user_id": user_id,
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
    query = usuarios_collection.where("username", "==", usuario.username).get()
    if not query:
        raise HTTPException(status_code=401, detail="Usuário ou Senha inválido!")

    user_doc = query[0]
    user = user_doc.to_dict()
    user_id = user_doc.id

    if not verificar_senha(usuario.password, user["salt"], user["password"]):
        raise HTTPException(status_code=401, detail="Usuário ou Senha inválido!")

    # Gera a chave temporária
    temp_key = generate_key(user_id)

    return {"message": "Login bem-sucedido", "key": temp_key}
