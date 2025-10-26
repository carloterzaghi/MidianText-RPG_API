"""
MidianText RPG - Cliente API Frontend
======================================

Este módulo fornece funções para comunicação entre o frontend (CustomTkinter)
e o backend (FastAPI) do jogo MidianText RPG.

Todas as funções fazem requisições HTTP para a API REST e retornam os resultados
em formato JSON. O tratamento de erros é padronizado, retornando um dicionário
com a chave "error" em caso de falha.

Módulos de Funcionalidade:
    - Autenticação: registro e login de usuários
    - Personagens: CRUD completo de personagens
    - Missões: acesso ao sistema de missões
    - Loja: transações da loja do jogo

Configuração:
    BASE_URL: Endpoint base da API (padrão: http://127.0.0.1:8000)

Author: Carlo Terzaghi
Version: 1.0
"""

import requests
from typing import Dict, Any, Optional

# URL base do servidor API backend
BASE_URL = "http://127.0.0.1:8000"


# ============================================================================
# AUTENTICAÇÃO
# ============================================================================

def register_user(username: str, password: str) -> Dict[str, Any]:
    """
    Registra um novo usuário no sistema.
    
    Envia uma requisição POST para criar uma nova conta de usuário no backend.
    A senha é hasheada no servidor antes de ser armazenada.
    
    Args:
        username (str): Nome de usuário único (2-20 caracteres)
        password (str): Senha do usuário (mínimo 6 caracteres)
    
    Returns:
        Dict[str, Any]: Resposta da API contendo:
            - Em sucesso: {"message": "Usuário criado com sucesso"}
            - Em erro: {"error": "mensagem de erro"}
    
    Example:
        >>> result = register_user("jogador1", "senha123")
        >>> if "error" not in result:
        ...     print("Usuário criado!")
    
    Notes:
        - Usernames devem ser únicos
        - Validações adicionais são feitas no backend
    """
    url = f"{BASE_URL}/register"
    data = {"username": username, "password": password}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Levanta exceção para status 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao registrar usuário: {e}")
        return {"error": str(e)}


def login_user(username: str, password: str) -> Dict[str, Any]:
    """
    Autentica um usuário e retorna um token de acesso JWT.
    
    Args:
        username (str): Nome de usuário
        password (str): Senha do usuário
    
    Returns:
        Dict[str, Any]: Resposta da API contendo:
            - Em sucesso: {
                "access_token": "token_jwt",
                "token_type": "bearer",
                "username": "nome_do_usuario"
              }
            - Em erro: {"error": "mensagem de erro"}
    
    Example:
        >>> result = login_user("jogador1", "senha123")
        >>> if "access_token" in result:
        ...     token = result["access_token"]
        ...     print(f"Login bem-sucedido! Token: {token}")
    
    Notes:
        - O token deve ser incluído em requisições autenticadas
        - Formato do header: Authorization: Bearer <token>
    """
    url = f"{BASE_URL}/login"
    data = {"username": username, "password": password}
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer login: {e}")
        return {"error": str(e)}


# ============================================================================
# GERENCIAMENTO DE PERSONAGENS
# ============================================================================

def get_personagens(token: str) -> Any:
    """
    Busca todos os personagens do usuário autenticado.
    
    Args:
        token (str): Token JWT de autenticação
    
    Returns:
        Any: Lista de personagens ou dicionário de erro:
            - Em sucesso: [
                {
                    "id": "uuid",
                    "name": "nome",
                    "character_class": "classe",
                    "level": 1,
                    "status": {...},
                    "itens": {...},
                    ...
                }
              ]
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> personagens = get_personagens(token)
        >>> if isinstance(personagens, list):
        ...     for char in personagens:
        ...         print(f"{char['name']} - Nível {char['level']}")
    
    Notes:
        - Retorna lista vazia [] se o usuário não tem personagens
        - Máximo de 3 personagens por usuário
    """
    url = f"{BASE_URL}/personagens"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar personagens: {e}")
        return {"error": str(e)}


def create_character(token: str, name: str, character_class: str, 
                    color: str = "cinza") -> Dict[str, Any]:
    """
    Cria um novo personagem para o usuário autenticado.
    
    Args:
        token (str): Token JWT de autenticação
        name (str): Nome do personagem (2-20 caracteres, único por usuário)
        character_class (str): Classe do personagem (Assassino, Arqueiro, Mago, Soldado)
        color (str, optional): Cor do personagem para sistema de vantagens.
            Opções: "vermelho", "verde", "azul", "cinza". Default: "cinza"
    
    Returns:
        Dict[str, Any]: Dados do personagem criado ou erro:
            - Em sucesso: {
                "id": "uuid",
                "name": "nome",
                "character_class": "classe",
                "level": 1,
                "color": "cor",
                "status": {stats completos},
                "itens": {itens iniciais},
                "habilidades": [lista de habilidades],
                ...
              }
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> char = create_character(token, "Herói", "Mago", "vermelho")
        >>> if "error" not in char:
        ...     print(f"Personagem {char['name']} criado!")
    
    Notes:
        - Sistema de cores: vermelho > verde > azul > vermelho (vantagem x1.5)
        - Cinza é neutro (sem vantagens)
        - Cada classe tem itens e habilidades únicas
        - Limite de 3 personagens por usuário
    """
    url = f"{BASE_URL}/personagens/criar"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"name": name, "character_class": character_class, "color": color}
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar personagem: {e}")
        return {"error": str(e)}

def get_available_classes() -> Dict[str, Any]:
    """
    Busca informações sobre todas as classes de personagem disponíveis.
    
    Returns:
        Dict[str, Any]: Dicionário com informações de cada classe:
            {
                "Assassino": {
                    "name": "Assassino",
                    "stats": {
                        "hp_max": int,
                        "strg": int,
                        "mag": int,
                        "spd": int,
                        "luck": int,
                        "defe": int,
                        "mov": int
                    },
                    "habilidades": [lista de habilidades]
                },
                "Arqueiro": {...},
                "Mago": {...},
                "Soldado": {...}
            }
        - Em erro: {"error": "mensagem"}
    
    Example:
        >>> classes = get_available_classes()
        >>> if "Mago" in classes:
        ...     print(f"HP do Mago: {classes['Mago']['stats']['hp_max']}")
    
    Notes:
        - Não requer autenticação
        - Útil para exibir informações antes da criação do personagem
    """
    url = f"{BASE_URL}/personagens/classes"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar classes: {e}")
        return {"error": str(e)}


def get_available_colors() -> Dict[str, Any]:
    """
    Busca informações sobre o sistema de cores e suas vantagens.
    
    Returns:
        Dict[str, Any]: Informações sobre cores e vantagens:
            {
                "cores": {
                    "vermelho": {"vence": "verde", ...},
                    "verde": {"vence": "azul", ...},
                    "azul": {"vence": "vermelho", ...},
                    "cinza": {"vence": null, "descrição": "Neutro"}
                },
                "multiplicador_vantagem": 1.5,
                "sistema": "Rock-Paper-Scissors"
            }
        - Em erro: {"error": "mensagem"}
    
    Example:
        >>> cores = get_available_colors()
        >>> print(f"Vermelho vence: {cores['cores']['vermelho']['vence']}")
    
    Notes:
        - Sistema baseado em Pedra-Papel-Tesoura
        - Vantagem concede 1.5x de dano
        - Cinza não tem vantagens nem desvantagens
    """
    url = f"{BASE_URL}/personagens/cores"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar cores: {e}")
        return {"error": str(e)}


def delete_character(token: str, character_name: str) -> Dict[str, Any]:
    """
    Deleta permanentemente um personagem do usuário autenticado.
    
    Args:
        token (str): Token JWT de autenticação
        character_name (str): Nome exato do personagem a ser deletado
    
    Returns:
        Dict[str, Any]: Confirmação ou erro:
            - Em sucesso: {"message": "Personagem 'nome' deletado com sucesso"}
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> result = delete_character(token, "Herói")
        >>> if "error" not in result:
        ...     print("Personagem deletado!")
    
    Warnings:
        - Esta ação é IRREVERSÍVEL
        - Remove o personagem e todos os seus dados
        - Nome deve corresponder exatamente (case-insensitive)
    
    Notes:
        - Libera espaço no limite de 3 personagens
        - Remove da estrutura antiga e nova do Firebase
    """
    url = f"{BASE_URL}/personagens/{character_name}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao deletar personagem: {e}")
        return {"error": str(e)}

# ============================================================================
# SISTEMA DE LOJA
# ============================================================================

def get_shop_items(token: str) -> Dict[str, Any]:
    """
    Busca todos os itens disponíveis na loja do jogo.
    
    Args:
        token (str): Token JWT de autenticação
    
    Returns:
        Dict[str, Any]: Catálogo de itens da loja:
            {
                "items": [
                    {
                        "name": "nome_do_item",
                        "description": "descrição",
                        "price": int,
                        "effect": {...},
                        "rarity": "common|rare|epic"
                    },
                    ...
                ]
            }
        - Em erro: {"error": "mensagem"}
    
    Example:
        >>> items = get_shop_items(token)
        >>> for item in items.get("items", []):
        ...     print(f"{item['name']}: {item['price']} gold")
    
    Notes:
        - Preços variam por raridade do item
        - Itens podem ter efeitos permanentes ou temporários
    """
    url = f"{BASE_URL}/shop/items"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar itens da loja: {e}")
        return {"error": str(e)}


def buy_item(token: str, character_name: str, item_name: str, 
             quantity: int = 1) -> Dict[str, Any]:
    """
    Compra um item da loja para um personagem.
    
    Args:
        token (str): Token JWT de autenticação
        character_name (str): Nome do personagem que comprará o item
        item_name (str): Nome do item a comprar
        quantity (int, optional): Quantidade a comprar. Default: 1
    
    Returns:
        Dict[str, Any]: Resultado da compra:
            - Em sucesso: {
                "message": "Item comprado com sucesso",
                "gold_remaining": int,
                "item_quantity": int
              }
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> result = buy_item(token, "Herói", "Poção de Cura", 5)
        >>> if "error" not in result:
        ...     print(f"Gold restante: {result['gold_remaining']}")
    
    Raises:
        - Erro se o personagem não tem gold suficiente
        - Erro se o item não existe na loja
    
    Notes:
        - O gold é deduzido automaticamente do personagem
        - Item é adicionado ao inventário
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
        print(f"Erro ao comprar item: {e}")
        return {"error": str(e)}


def sell_item(token: str, character_name: str, item_name: str, 
              quantity: int = 1) -> Dict[str, Any]:
    """
    Vende um item do inventário do personagem.
    
    Args:
        token (str): Token JWT de autenticação
        character_name (str): Nome do personagem que venderá o item
        item_name (str): Nome do item a vender
        quantity (int, optional): Quantidade a vender. Default: 1
    
    Returns:
        Dict[str, Any]: Resultado da venda:
            - Em sucesso: {
                "message": "Item vendido com sucesso",
                "gold_earned": int,
                "total_gold": int
              }
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> result = sell_item(token, "Herói", "Espada Velha", 1)
        >>> if "error" not in result:
        ...     print(f"Gold ganho: {result['gold_earned']}")
    
    Raises:
        - Erro se o personagem não possui o item
        - Erro se a quantidade é maior que a disponível
    
    Notes:
        - Preço de venda é geralmente 50% do preço de compra
        - Gold é adicionado automaticamente ao personagem
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
        print(f"Erro ao vender item: {e}")
        return {"error": str(e)}


def get_character_inventory(token: str, character_name: str) -> Dict[str, Any]:
    """
    Busca o inventário completo de um personagem específico.
    
    Args:
        token (str): Token JWT de autenticação
        character_name (str): Nome do personagem
    
    Returns:
        Dict[str, Any]: Dados do personagem incluindo inventário:
            {
                "name": "nome",
                "itens": {
                    "item1": quantidade,
                    "item2": quantidade,
                    ...
                },
                "gold": int,
                ...outros dados do personagem
            }
        - Em erro: {"error": "mensagem"}
    
    Example:
        >>> char = get_character_inventory(token, "Herói")
        >>> if "itens" in char:
        ...     for item, qty in char["itens"].items():
        ...         print(f"{item}: {qty}")
    
    Notes:
        - Retorna todos os dados do personagem, não apenas inventário
        - Útil para sincronizar dados após compras/vendas
    """
    url = f"{BASE_URL}/personagens/{character_name}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar inventário: {e}")
        return {"error": str(e)}


def get_character_gold(token: str, character_name: str) -> Dict[str, Any]:
    """
    Busca a quantidade de gold de um personagem.
    
    Args:
        token (str): Token JWT de autenticação
        character_name (str): Nome do personagem
    
    Returns:
        Dict[str, Any]: Gold do personagem:
            - Em sucesso: {"gold": int}
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> result = get_character_gold(token, "Herói")
        >>> if "gold" in result:
        ...     print(f"Gold disponível: {result['gold']}")
    
    Notes:
        - Mais eficiente que buscar todo o inventário
        - Atualizado em tempo real após transações
    """
    url = f"{BASE_URL}/personagens/{character_name}/gold"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar gold: {e}")
        return {"error": str(e)}

# ============================================================================
# SISTEMA DE MISSÕES
# ============================================================================

def get_missions(token: str) -> Dict[str, Any]:
    """
    Busca todas as missões disponíveis no jogo.
    
    Args:
        token (str): Token JWT de autenticação
    
    Returns:
        Dict[str, Any]: Lista de missões disponíveis:
            {
                "missions": [
                    {
                        "id": "mission_id",
                        "name": "nome_da_missão",
                        "description": "descrição",
                        "difficulty": "easy|medium|hard",
                        "rewards": {
                            "gold": int,
                            "exp": int,
                            "items": [...]
                        },
                        "requirements": {...}
                    },
                    ...
                ]
            }
        - Em erro: {"error": "mensagem"}
    
    Example:
        >>> missions = get_missions(token)
        >>> for mission in missions.get("missions", []):
        ...     print(f"{mission['name']} - {mission['difficulty']}")
    
    Notes:
        - Missões podem ter requisitos de nível
        - Dificuldade afeta recompensas e desafios
    """
    url = f"{BASE_URL}/missions"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar missões: {e}")
        return {"error": str(e)}


def start_mission(token: str, character_name: str, mission_id: str) -> Dict[str, Any]:
    """
    Inicia uma missão com um personagem.
    
    Args:
        token (str): Token JWT de autenticação
        character_name (str): Nome do personagem que iniciará a missão
        mission_id (str): ID da missão a iniciar
    
    Returns:
        Dict[str, Any]: Status inicial da missão:
            - Em sucesso: {
                "message": "Missão iniciada",
                "mission_state": {
                    "position": [x, y],
                    "enemies": [...],
                    "treasures": [...],
                    "map": [[...]],
                    "turns_remaining": int
                }
              }
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> result = start_mission(token, "Herói", "dungeon_1")
        >>> if "mission_state" in result:
        ...     print(f"Missão iniciada! Posição: {result['mission_state']['position']}")
    
    Raises:
        - Erro se o personagem não atende aos requisitos
        - Erro se a missão já está ativa
        - Erro se o personagem está em outra missão
    
    Notes:
        - Apenas uma missão ativa por personagem
        - Estado da missão é persistido automaticamente
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
        print(f"Erro ao iniciar missão: {e}")
        return {"error": str(e)}


def mission_action(token: str, character_name: str, mission_id: str, 
                   action: str, target: Optional[str] = None) -> Dict[str, Any]:
    """
    Executa uma ação durante uma missão.
    
    Args:
        token (str): Token JWT de autenticação
        character_name (str): Nome do personagem
        mission_id (str): ID da missão ativa
        action (str): Ação a executar. Opções:
            - 'move': Mover para uma direção
            - 'fight': Atacar um inimigo
            - 'collect': Coletar um tesouro
            - 'flee': Fugir da missão
        target (str, optional): Alvo da ação:
            - Para 'move': direção ('north', 'south', 'east', 'west')
            - Para 'fight': ID do inimigo
            - Para 'collect': ID do tesouro
            - Para 'flee': None
    
    Returns:
        Dict[str, Any]: Resultado da ação:
            - Em sucesso: {
                "message": "Ação executada",
                "result": {...},
                "mission_state": {estado atualizado},
                "combat_log": [...] (se aplicável),
                "mission_complete": bool
              }
            - Em erro: {"error": "mensagem"}
    
    Example:
        >>> # Mover para norte
        >>> result = mission_action(token, "Herói", "dungeon_1", "move", "north")
        >>> 
        >>> # Atacar inimigo
        >>> result = mission_action(token, "Herói", "dungeon_1", "fight", "enemy_1")
        >>> if result.get("mission_complete"):
        ...     print("Missão completada!")
    
    Raises:
        - Erro se a ação é inválida
        - Erro se o alvo não existe
        - Erro se o personagem não está na missão
    
    Notes:
        - Cada ação consome um turno
        - Combates são resolvidos automaticamente
        - Missão pode terminar por vitória, derrota ou fuga
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
        print(f"Erro ao executar ação da missão: {e}")
        return {"error": str(e)}


def get_mission_details(token: str, mission_id: str) -> Dict[str, Any]:
    """
    Busca detalhes completos de uma missão específica.
    
    Args:
        token (str): Token JWT de autenticação
        mission_id (str): ID da missão
    
    Returns:
        Dict[str, Any]: Detalhes completos da missão:
            {
                "id": "mission_id",
                "name": "nome",
                "description": "descrição detalhada",
                "difficulty": "easy|medium|hard",
                "map_size": [width, height],
                "enemies": [{tipo, stats, ...}, ...],
                "rewards": {
                    "gold": int,
                    "exp": int,
                    "items": [...]
                },
                "requirements": {
                    "min_level": int,
                    "recommended_class": [...]
                },
                "lore": "história da missão"
            }
        - Em erro: {"error": "mensagem"}
    
    Example:
        >>> details = get_mission_details(token, "dungeon_1")
        >>> if "requirements" in details:
        ...     print(f"Nível mínimo: {details['requirements']['min_level']}")
    
    Notes:
        - Não requer que a missão esteja ativa
        - Útil para exibir informações antes de iniciar
    """
    url = f"{BASE_URL}/missions/{mission_id}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes da missão: {e}")
        return {"error": str(e)}
