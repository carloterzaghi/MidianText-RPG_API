import requests

BASE_URL = "http://127.0.0.1:8000"

def register_user(username, password):
    """
    Registers a new user with the backend API.
    """
    url = f"{BASE_URL}/register"
    data = {"username": username, "password": password}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def login_user(username, password):
    """
    Logs in a user and retrieves an access token.
    """
    url = f"{BASE_URL}/login"
    data = {"username": username, "password": password}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def get_personagens(token):
    """
    Fetches the list of 'personagens' using an access token.
    """
    url = f"{BASE_URL}/personagens"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def create_character(token, name, character_class, color="cinza"):
    """
    Creates a new character for the authenticated user.
    """
    url = f"{BASE_URL}/personagens/criar"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "character_class": character_class, "color": color}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def get_available_classes():
    """
    Fetches the available character classes with their stats.
    """
    url = f"{BASE_URL}/personagens/classes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def get_available_colors():
    """
    Fetches the available character colors with their advantages.
    """
    url = f"{BASE_URL}/personagens/cores"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
