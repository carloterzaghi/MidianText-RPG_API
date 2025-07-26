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

def get_personagens(username):
    url = f"{BASE_URL}/personagens/{username}"
    response = requests.get(url)
    return response.json()

def main():
    while True:
        print("Bem-vindo ao MidianText RPG!")
        print("1. Registrar")
        print("2. Login")
        print("3. Sair")
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
            if "message" in result and "bem-sucedido" in result["message"]:
                personagens = get_personagens(username)
                print("Personagens:", personagens)
        elif choice == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
