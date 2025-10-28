"""
MidianText RPG - Gerenciador de Tokens JWT
===========================================

Este módulo é responsável pela geração e validação de tokens JWT (JSON Web Tokens)
utilizados para autenticação stateless na API.

Funcionalidades:
    - Geração de tokens assinados para usuários autenticados
    - Validação de tokens com verificação de expiração
    - Suporte a variáveis de ambiente para chave secreta

Segurança:
    - Tokens assinados com chave secreta (SECRET_KEY)
    - Expiração configurável (padrão: 2 horas)
    - Serialização segura via ITSDangerous
    - Proteção contra adulteração de tokens

Fluxo de Autenticação:
    1. Usuário faz login → Backend valida credenciais
    2. generate_key() cria token com user_id
    3. Token enviado ao cliente → Armazenado no frontend
    4. Requisições posteriores incluem token no header Authorization
    5. verify_key() valida token em cada requisição protegida

Environment Variables:
    SECRET_KEY: Chave secreta para assinatura de tokens
                (use valor forte em produção!)

Dependencies: itsdangerous, python-dotenv
"""

from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

# Chave secreta para assinar os tokens JWT
# IMPORTANTE: Em produção, sempre use uma chave forte via variável de ambiente
SECRET_KEY = os.getenv(
    'SECRET_KEY', 
    'dev-secret-key-midiantext-rpg-2025-change-in-production'
)

# Serializer para gerar e verificar tokens com tempo de expiração
# URLSafeTimedSerializer garante tokens seguros e URL-safe
serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_key(user_id: str) -> str:
    """
    Gera um token JWT temporário para um ID de usuário.
    
    O token é assinado com a chave secreta e pode ser verificado posteriormente
    para autenticar requisições. Não armazena informações sensíveis.
    
    Args:
        user_id (str): Identificador único do usuário (ID do documento Firestore)
    
    Returns:
        str: Token JWT assinado, codificado de forma segura para URLs
    
    Example:
        >>> token = generate_key("abc123def456")
        >>> print(token)
        'InNvbWUgdG9rZW4gZGF0YSI.DdUOIA.W7rHbQK...'
    
    Notes:
        - Token não expira na geração (expiração verificada em verify_key)
        - Token é stateless (não armazenado no servidor)
        - Pode ser decodificado sem a chave, mas não adulterado
    """
    return serializer.dumps(user_id)


def verify_key(key: str) -> str | None:
    """
    Verifica se um token JWT é válido e não expirou.
    
    Decodifica e valida o token, verificando:
    - Assinatura (token não foi adulterado)
    - Expiração (token ainda está dentro do prazo válido)
    
    Args:
        key (str): Token JWT a ser validado
    
    Returns:
        str | None: 
            - ID do usuário (str) se token válido
            - None se token inválido, expirado ou adulterado
    
    Raises:
        Não lança exceções - retorna None em caso de erro
    
    Example:
        >>> user_id = verify_key(token)
        >>> if user_id:
        ...     print(f"Usuário autenticado: {user_id}")
        ... else:
        ...     print("Token inválido")
    
    Notes:
        - Expiração: 2 horas (7200 segundos) após geração
        - Logs de debug podem ser removidos em produção
        - Em caso de falha, sempre retorna None (seguro por padrão)
    """
    try:
        print(f"DEBUG verify_key: Attempting to verify token")
        
        # Verifica o token com tempo de expiração de 2 horas (7200 segundos)
        # max_age: tempo máximo (em segundos) desde a criação do token
        user_id = serializer.loads(key, max_age=7200)
        
        print(f"DEBUG verify_key: Token valid, user_id: {user_id}")
        return user_id
    
    except Exception as e:
        # Captura qualquer erro (expiração, assinatura inválida, formato incorreto)
        print(f"DEBUG verify_key: Token validation failed - {type(e).__name__}: {str(e)}")
        return None
