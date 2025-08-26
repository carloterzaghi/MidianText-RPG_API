import requests

BASE_URL = "http://127.0.0.1:8000"

def register_user(username, password):
    url = f"{BASE_URL}/register"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json()

def login_user(username, password):
    url = f"{BASE_URL}/login"
    data = {"username": username, "password": password}
    response = requests.post(url, json=data)
    return response.json()

def get_personagens(token):
    url = f"{BASE_URL}/personagens"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def main():
    token = None
    while True:
        print("Bem-vindo ao MidianText RPG!")
        print("1. Registrar")
        print("2. Login")
        print("3. Ver Personagens")
        print("4. Deslogar")
        print("5. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            username = input("Digite seu nome de usuário: ")
            password = input("Digite sua senha: ")
            result = register_user(username, password)
            print(result)
        elif choice == '2':
            username = input("Digite seu nome de usuário: ")
            password = input("Digite sua senha: ")
            result = login_user(username, password)
            print(result)
            if "key" in result:
                token = result["key"]
                print("Login realizado com sucesso!")
            else:
                print("Falha no login.")
        elif choice == '3':
            if not token:
                print("Você precisa estar logado para ver seus personagens.")
            else:
                personagens = get_personagens(token)
                print("Personagens:", personagens)
        elif choice == '4':
            if token:
                token = None
                print("Você foi deslogado com sucesso.")
            else:
                print("Você já está deslogado.")
        elif choice == '5':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
