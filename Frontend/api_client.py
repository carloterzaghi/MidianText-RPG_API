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

def delete_character(token, character_name):
    """
    Deletes a character for the authenticated user.
    """
    url = f"{BASE_URL}/personagens/{character_name}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

# ==================== Funções da Loja ====================

def get_shop_items(token):
    """
    Fetches all items available in the shop.
    """
    url = f"{BASE_URL}/shop/items"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def buy_item(token, character_name, item_name, quantity=1):
    """
    Buys an item from the shop for a character.
    
    Args:
        token: Access token
        character_name: Name of the character
        item_name: Name of the item to buy
        quantity: Quantity to buy (default: 1)
    """
    url = f"{BASE_URL}/shop/buy"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "character_name": character_name,
        "item_name": item_name,
        "quantity": quantity
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def sell_item(token, character_name, item_name, quantity=1):
    """
    Sells an item from character's inventory.
    
    Args:
        token: Access token
        character_name: Name of the character
        item_name: Name of the item to sell
        quantity: Quantity to sell (default: 1)
    """
    url = f"{BASE_URL}/shop/sell"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "character_name": character_name,
        "item_name": item_name,
        "quantity": quantity
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def get_character_inventory(token, character_name):
    """
    Fetches the inventory of a specific character.
    
    Args:
        token: Access token
        character_name: Name of the character
    """
    url = f"{BASE_URL}/personagens/{character_name}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def get_character_gold(token, character_name):
    """
    Fetches the gold of a specific character.
    
    Args:
        token: Access token
        character_name: Name of the character
    """
    url = f"{BASE_URL}/personagens/{character_name}/gold"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

# ==================== Funções de Missões ====================

def get_missions(token):
    """
    Fetches all available missions.
    """
    url = f"{BASE_URL}/missions"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def start_mission(token, character_name, mission_id):
    """
    Starts a mission for a character.
    
    Args:
        token: Access token
        character_name: Name of the character
        mission_id: ID of the mission to start
    """
    url = f"{BASE_URL}/missions/start"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "character_name": character_name,
        "mission_id": mission_id
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def mission_action(token, character_name, mission_id, action, target=None):
    """
    Performs an action during a mission.
    
    Args:
        token: Access token
        character_name: Name of the character
        mission_id: ID of the mission
        action: Action to perform ('move', 'fight', 'collect')
        target: Target of the action (direction, enemy_id, or treasure_id)
    """
    url = f"{BASE_URL}/missions/action"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "character_name": character_name,
        "mission_id": mission_id,
        "action": action,
        "target": target
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}

def get_mission_details(token, mission_id):
    """
    Fetches details of a specific mission.
    
    Args:
        token: Access token
        mission_id: ID of the mission
    """
    url = f"{BASE_URL}/missions/{mission_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {"error": str(e)}
