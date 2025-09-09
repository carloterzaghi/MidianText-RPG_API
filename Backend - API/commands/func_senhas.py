import hashlib
import os

def hash_senha(senha: str) -> tuple:
    """
    Gera um hash seguro da senha usando PBKDF2 com SHA-256.

    Parâmetros:
        senha (str): A senha em texto plano que será protegida.

    Retorna:
        tuple: Um par contendo:
            - salt (str): O salt gerado, codificado em hexadecimal.
            - senha_hash (str): A senha com hash e salt, codificada em hexadecimal.
    """
    salt = os.urandom(16)
    senha_hash = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt, 100000)
    return salt.hex(), senha_hash.hex()

def verificar_senha(senha: str, salt: str, senha_hash: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash armazenado.

    Parâmetros:
        senha (str): A senha em texto plano fornecida pelo usuário.
        salt (str): O salt armazenado.
        senha_hash (str): O hash da senha armazenado.

    Retorna:
        bool: True se a senha estiver correta, False caso contrário.
    """
    salt_bytes = bytes.fromhex(salt)
    senha_hash_bytes = bytes.fromhex(senha_hash)
    
    # Hash da senha fornecida com o mesmo salt
    nova_senha_hash = hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), salt_bytes, 100000)
    
    return nova_senha_hash == senha_hash_bytes
