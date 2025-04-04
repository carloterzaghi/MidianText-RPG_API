import bcrypt

def hash_senha(senha: str) -> tuple:
    """
    Gera um hash seguro da senha usando bcrypt com um salt aleatório.

    Parâmetros:
        senha (str): A senha em texto plano que será protegida.

    Retorna:
        tuple: Um par contendo:
            - salt (str): O salt gerado, codificado em base64.
            - senha_hashed (str): A senha protegida com hash e salt.

    Exemplo de uso:
        salt, senha_hashed = hash_senha("minha_senha123")
    """
    salt = bcrypt.gensalt()  # Gerando um salt aleatório
    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)  # Hash com salt
    return salt.decode('utf-8'), senha_hashed.decode('utf-8')

def verificar_senha(senha: str, salt: str, senha_hashed: str) -> bool:
    """
    Verifica se uma senha em texto plano corresponde ao hash armazenado.

    Parâmetros:
        senha (str): A senha em texto plano fornecida pelo usuário.
        salt (str): O salt original armazenado.
        senha_hashed (str): O hash da senha armazenado.

    Retorna:
        bool: True se a senha estiver correta, False caso contrário.

    Exemplo de uso:
        if verificar_senha("minha_senha123", salt, senha_hashed):
            print("Senha correta!")
        else:
            print("Senha incorreta!")
    """
    return bcrypt.checkpw(senha.encode('utf-8'), senha_hashed.encode('utf-8'))
