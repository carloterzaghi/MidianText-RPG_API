from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Chave secreta para assinar os tokens
# Use uma chave fixa do ambiente ou uma padrão para desenvolvimento
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-midiantext-rpg-2025-change-in-production')

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
        print(f"DEBUG verify_key: Attempting to verify token")
        # Verifica o token com um tempo de expiração de 2 horas (7200 segundos)
        user_id = serializer.loads(key, max_age=7200)
        print(f"DEBUG verify_key: Token valid, user_id: {user_id}")
        return user_id
    except Exception as e:
        print(f"DEBUG verify_key: Token validation failed - {type(e).__name__}: {str(e)}")
        return None
