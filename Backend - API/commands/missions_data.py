"""
Banco de dados de missões disponíveis
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

def get_mission(mission_id: str):
    """Retorna os dados de uma missão"""
    return MISSIONS.get(mission_id)

def get_all_missions():
    """Retorna todas as missões disponíveis"""
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
