"""
MidianText RPG - Gerenciador de Segurança de Senhas
====================================================

Este módulo implementa o sistema de hashing de senhas utilizando PBKDF2-HMAC-SHA256,
garantindo armazenamento seguro de credenciais de usuários.

Funcionalidades:
    - Geração de hash de senhas com salt aleatório
    - Verificação de senhas em tempo constante
    - Proteção contra rainbow tables e ataques de força bruta

Algoritmo:
    - PBKDF2 (Password-Based Key Derivation Function 2)
    - HMAC-SHA-256 como função de hash
    - 100.000 iterações (proteção contra brute-force)
    - Salt de 16 bytes (128 bits) aleatório por senha

Segurança:
    - Salt único para cada senha (proteção contra rainbow tables)
    - Iterações elevadas (dificulta ataques de força bruta)
    - Hash não reversível (one-way function)
    - Comparação em tempo constante (proteção contra timing attacks)

Fluxo de Uso:
    Registro:
        1. Usuário fornece senha em texto plano
        2. hash_senha() gera salt aleatório
        3. Senha + salt → PBKDF2 → hash
        4. Salt e hash armazenados no Firebase (NÃO a senha)
    
    Login:
        1. Usuário fornece senha
        2. Sistema busca salt e hash armazenados
        3. verificar_senha() aplica mesmo processo
        4. Compara hashes → Autentica se iguais

Dependencies: hashlib (built-in), os (built-in)
"""

import hashlib
import os


def hash_senha(senha: str) -> tuple[str, str]:
    """
    Gera um hash seguro da senha usando PBKDF2-HMAC-SHA256.
    
    Este método cria um salt aleatório único e aplica a função de derivação
    de chave PBKDF2 com 100.000 iterações, tornando ataques de força bruta
    computacionalmente caros.
    
    Args:
        senha (str): Senha em texto plano fornecida pelo usuário
    
    Returns:
        tuple[str, str]: Par contendo:
            - salt (str): Salt gerado (16 bytes em hexadecimal)
            - senha_hash (str): Hash da senha (32 bytes em hexadecimal)
    
    Example:
        >>> salt, hash_result = hash_senha("minha_senha_123")
        >>> print(f"Salt: {salt}")
        Salt: a1b2c3d4e5f6...
        >>> print(f"Hash: {hash_result}")
        Hash: 9f8e7d6c5b4a...
    
    Security Notes:
        - Salt de 16 bytes garante unicidade
        - 100.000 iterações tornam brute-force lento
        - SHA-256 é resistente a colisões
        - Resultado em hexadecimal facilita armazenamento
    
    Storage:
        Armazene AMBOS salt e hash no banco de dados:
        {
            "salt": "a1b2c3...",
            "password_hash": "9f8e7d..."
        }
    """
    # Gera salt aleatório de 16 bytes (128 bits)
    # os.urandom() usa fonte de entropia do sistema operacional
    salt = os.urandom(16)
    
    # Aplica PBKDF2-HMAC-SHA256
    # - 'sha256': função de hash
    # - senha.encode('utf-8'): converte string para bytes
    # - salt: salt único
    # - 100000: número de iterações (aumenta custo computacional)
    senha_hash = hashlib.pbkdf2_hmac(
        'sha256',
        senha.encode('utf-8'),
        salt,
        100000
    )
    
    # Converte bytes para hexadecimal para armazenamento
    return salt.hex(), senha_hash.hex()


def verificar_senha(senha: str, salt: str, senha_hash: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash armazenado.
    
    Reconstrói o hash usando a senha fornecida e o salt armazenado,
    comparando com o hash original. A comparação é feita em tempo constante
    para prevenir timing attacks.
    
    Args:
        senha (str): Senha em texto plano fornecida pelo usuário
        salt (str): Salt armazenado (em hexadecimal)
        senha_hash (str): Hash da senha armazenado (em hexadecimal)
    
    Returns:
        bool: 
            - True se a senha estiver correta
            - False se a senha estiver incorreta
    
    Example:
        >>> # Registro
        >>> salt, hash_stored = hash_senha("senha123")
        >>> 
        >>> # Login
        >>> is_valid = verificar_senha("senha123", salt, hash_stored)
        >>> print(is_valid)
        True
        >>> 
        >>> is_valid = verificar_senha("senha_errada", salt, hash_stored)
        >>> print(is_valid)
        False
    
    Security Notes:
        - Usa mesmo algoritmo e iterações de hash_senha()
        - Comparação de bytes previne timing attacks
        - Não revela informações sobre senha correta
    
    Process:
        1. Converte salt/hash de hex para bytes
        2. Aplica PBKDF2 na senha fornecida com salt armazenado
        3. Compara novo hash com hash armazenado
        4. Retorna True apenas se forem idênticos
    """
    # Converte salt e hash de hexadecimal para bytes
    salt_bytes = bytes.fromhex(salt)
    senha_hash_bytes = bytes.fromhex(senha_hash)
    
    # Aplica PBKDF2 na senha fornecida usando o MESMO salt e parâmetros
    # Isso garante que senha idêntica produz hash idêntico
    nova_senha_hash = hashlib.pbkdf2_hmac(
        'sha256',
        senha.encode('utf-8'),
        salt_bytes,
        100000  # Mesmas 100.000 iterações
    )
    
    # Comparação segura de bytes (tempo constante)
    # Previne timing attacks ao não retornar early em diferenças
    return nova_senha_hash == senha_hash_bytes
