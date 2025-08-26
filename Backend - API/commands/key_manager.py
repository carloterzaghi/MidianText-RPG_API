from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import secrets

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Chave secreta para assinar os tokens
SECRET_KEY = secrets.token_urlsafe(32)

# Serializer para gerar e verificar tokens com tempo de expiração
serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_key(user_id: str) -> str:
    """
    Gera uma chave temporária (token) para um ID de usuário.
    A chave expira em 30 minutos (1800 segundos).

    Parâmetros:
        user_id (str): O ID do usuário.

    Retorna:
        str: A chave temporária gerada.
    """
    return serializer.dumps(user_id)

def verify_key(key: str) -> str | None:
    """
    Verifica se uma chave temporária é válida e não expirou.

    Parâmetros:
        key (str): A chave temporária a ser verificada.

    Retorna:
        str | None: O ID do usuário se a chave for válida, ou None caso contrário.
    """
    try:
        # Verifica o token com um tempo de expiração de 30 minutos
        user_id = serializer.loads(key, max_age=1800)
        return user_id
    except Exception:
        return None
