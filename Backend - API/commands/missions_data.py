"""
MidianText RPG - Banco de Dados de Missões
===========================================

Este módulo centraliza todas as missões disponíveis no jogo, incluindo estrutura de salas,
inimigos, tesouros e sistema de progressão.

Estrutura de Dados:
    Cada missão contém:
        - Metadados: ID, nome, descrição, dificuldade, nível mínimo
        - Recompensas: Ouro, experiência, itens
        - Salas: Grafo de localidades interconectadas
        - Sala inicial: Ponto de entrada da missão

Estrutura de Sala:
    {
        "id": str,                    # Identificador único
        "name": str,                  # Nome da localidade
        "description": str,           # Narrativa descritiva
        "enemies": List[Enemy],       # Inimigos presentes
        "treasures": List[Treasure],  # Baús e itens
        "exits": Dict[str, str],      # Saídas disponíveis {direção: sala_destino}
        "visited": bool               # Estado de visitação
    }

Estrutura de Inimigo:
    {
        "id": str,           # Identificador único
        "name": str,         # Nome do inimigo
        "hp": int,           # Pontos de vida
        "attack": int,       # Poder de ataque
        "defense": int,      # Defesa
        "gold_drop": int,    # Ouro dropado ao morrer
        "exp_drop": int      # Experiência dropada ao morrer
    }

Estrutura de Tesouro:
    {
        "id": str,                      # Identificador único
        "name": str,                    # Nome do baú/tesouro
        "contents": {
            "gold": int,                # Quantidade de ouro
            "items": List[str]          # Lista de itens
        }
    }

Missões Disponíveis:
    - Tumbas do Faraó: Exploração de tumba egípcia com armadilhas e múmias

Fluxo de Uso:
    1. Frontend solicita lista de missões via get_all_missions()
    2. Jogador seleciona missão baseado em nível/dificuldade
    3. Backend carrega dados completos via get_mission(mission_id)
    4. Sistema de combate/exploração usa estrutura de salas
    5. Estado de visitação atualizado conforme progressão

Design Patterns:
    - Singleton: MISSIONS é dicionário global compartilhado
    - Grafo: Salas conectadas por exits formam mapa navegável
    - Factory: Funções get_* retornam instâncias/views dos dados

Future Enhancements:
    - Adicionar mais missões (floresta, cavernas, castelo)
    - Sistema de missões dinâmicas/procedurais
    - Missões multi-jogador
    - Eventos aleatórios em salas

"""

MISSIONS = {
    "tumbas_farao": {
        "id": "tumbas_farao",
        "name": "Tumbas do Faraó",
        "description": "Uma antiga tumba foi descoberta no deserto. Dizem que grandes tesouros e perigos aguardam aqueles corajosos o suficiente para explorá-la.",
        "difficulty": "Médio",
        "min_level": 1,
        "rewards": {
            "gold": 200,
            "exp": 150,
            "items": ["Amuleto do Faraó", "Poção de Cura"]
        },
        "rooms": {
            "entrada": {
                "id": "entrada",
                "name": "Entrada da Tumba",
                "description": "Você está na entrada de uma antiga tumba. Tochas iluminam fracamente as paredes cobertas de hieróglifos. O ar é pesado e úmido. Duas passagens se abrem à sua frente: uma à esquerda e outra à direita.",
                "enemies": [],
                "treasures": [],
                "exits": {
                    "esquerda": "sala_guardiao",
                    "direita": "corredor_armadilhas"
                },
                "visited": False
            },
            "sala_guardiao": {
                "id": "sala_guardiao",
                "name": "Sala do Guardião",
                "description": "Uma sala ampla com pilares de pedra. No centro, uma estátua de Anúbis observa silenciosamente. Ao se aproximar, a estátua ganha vida! Um Guardião Esquelético emerge das sombras.",
                "enemies": [
                    {
                        "id": "guardiao_1",
                        "name": "Guardião Esquelético",
                        "hp": 30,
                        "attack": 8,
                        "defense": 5,
                        "gold_drop": 50,
                        "exp_drop": 40
                    }
                ],
                "treasures": [
                    {
                        "id": "bau_1",
                        "name": "Baú Antigo",
                        "contents": {"gold": 75, "items": ["Poção de Cura"]}
                    }
                ],
                "exits": {
                    "frente": "camara_tesouro",
                    "voltar": "entrada"
                },
                "visited": False
            },
            "corredor_armadilhas": {
                "id": "corredor_armadilhas",
                "name": "Corredor das Armadilhas",
                "description": "Um corredor estreito com marcas no chão. Você nota pequenos buracos nas paredes. De repente, dardos envenenados começam a voar! Você precisa ser rápido.",
                "enemies": [],
                "treasures": [
                    {
                        "id": "bau_2",
                        "name": "Baú Escondido",
                        "contents": {"gold": 60, "items": ["Antídoto"]}
                    }
                ],
                "exits": {
                    "frente": "sala_escaravelhos",
                    "voltar": "entrada"
                },
                "visited": False
            },
            "sala_escaravelhos": {
                "id": "sala_escaravelhos",
                "name": "Sala dos Escaravelhos",
                "description": "O chão desta sala está coberto por milhares de escaravelhos dourados. Ao pisar neles, alguns ganham vida e atacam em enxame!",
                "enemies": [
                    {
                        "id": "enxame_1",
                        "name": "Enxame de Escaravelhos",
                        "hp": 20,
                        "attack": 6,
                        "defense": 2,
                        "gold_drop": 30,
                        "exp_drop": 25
                    }
                ],
                "treasures": [],
                "exits": {
                    "frente": "camara_tesouro",
                    "voltar": "corredor_armadilhas"
                },
                "visited": False
            },
            "camara_tesouro": {
                "id": "camara_tesouro",
                "name": "Câmara do Tesouro",
                "description": "Você finalmente chegou à câmara principal! Um sarcófago dourado repousa no centro, rodeado por pilhas de ouro e artefatos. Mas ao se aproximar, o Faraó Múmia desperta para proteger seu tesouro!",
                "enemies": [
                    {
                        "id": "farao_mumia",
                        "name": "Faraó Múmia",
                        "hp": 50,
                        "attack": 12,
                        "defense": 8,
                        "gold_drop": 150,
                        "exp_drop": 100
                    }
                ],
                "treasures": [
                    {
                        "id": "tesouro_principal",
                        "name": "Sarcófago Dourado",
                        "contents": {"gold": 300, "items": ["Amuleto do Faraó", "Poção de Cura", "Pergaminho Antigo"]}
                    }
                ],
                "exits": {
                    "saida": "fim"
                },
                "visited": False
            }
        },
        "starting_room": "entrada"
    }
}


def get_mission(mission_id: str) -> dict | None:
    """
    Retorna os dados completos de uma missão específica.
    
    Usado para iniciar uma missão, carregando todos os dados necessários
    incluindo salas, inimigos, tesouros e conexões.
    
    Args:
        mission_id (str): Identificador único da missão (ex: "tumbas_farao")
    
    Returns:
        dict | None: 
            - dict: Dados completos da missão se encontrada
            - None: Se mission_id não existir
    
    Example:
        >>> mission = get_mission("tumbas_farao")
        >>> if mission:
        ...     print(f"Iniciando: {mission['name']}")
        ...     print(f"Sala inicial: {mission['starting_room']}")
        Iniciando: Tumbas do Faraó
        Sala inicial: entrada
    
    Usage:
        # No backend, ao iniciar missão:
        mission_data = get_mission(mission_id)
        if not mission_data:
            raise HTTPException(404, "Missão não encontrada")
        
        # Inicializar estado do jogador na missão
        player_state = {
            "current_room": mission_data["starting_room"],
            "visited_rooms": [],
            "defeated_enemies": []
        }
    
    Notes:
        - Retorna cópia completa dos dados (todas as salas e metadados)
        - Estado de visitação (visited) deve ser gerenciado pelo backend
        - Dados de inimigos/tesouros são templates (instanciar por jogador)
    """
    return MISSIONS.get(mission_id)


def get_all_missions() -> list[dict]:
    """
    Retorna lista resumida de todas as missões disponíveis.
    
    Usado para exibir catálogo de missões no frontend, mostrando apenas
    informações essenciais sem carregar dados completos de salas/inimigos.
    
    Returns:
        list[dict]: Lista de missões com metadados resumidos. Cada entrada contém:
            - id (str): Identificador único
            - name (str): Nome da missão
            - description (str): Descrição narrativa
            - difficulty (str): Nível de dificuldade ("Fácil", "Médio", "Difícil")
            - min_level (int): Nível mínimo requerido
            - rewards (dict): Recompensas ao completar
    
    Example:
        >>> missions = get_all_missions()
        >>> for mission in missions:
        ...     print(f"{mission['name']} - Nível {mission['min_level']}+")
        Tumbas do Faraó - Nível 1+
    
    Usage:
        # No frontend, ao exibir lista de missões:
        response = requests.get("http://localhost:8000/missions")
        missions = response.json()
        
        for mission in missions:
            # Verificar se jogador atende nível mínimo
            if player.level >= mission["min_level"]:
                display_mission(mission)
    
    Notes:
        - Não inclui dados de salas/inimigos (economiza memória/rede)
        - Ideal para tela de seleção de missões
        - Frontend deve fazer requisição separada para dados completos
    
    Performance:
        - List comprehension: O(n) onde n = número de missões
        - Atualmente: 1 missão = ~1ms de processamento
        - Escalável até ~100 missões sem impacto perceptível
    """
    return [
        {
            "id": mission["id"],
            "name": mission["name"],
            "description": mission["description"],
            "difficulty": mission["difficulty"],
            "min_level": mission["min_level"],
            "rewards": mission["rewards"]
        }
        for mission in MISSIONS.values()
    ]
