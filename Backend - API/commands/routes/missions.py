from fastapi import APIRouter, HTTPException, Header
from commands.database import personagens_collection
from commands.key_manager import verify_key
from commands.missions_data import get_mission, get_all_missions
from commands.models.mission_model import (
    StartMissionRequest, 
    MissionActionRequest, 
    MissionActionResponse
)
from google.cloud import firestore
import copy

router = APIRouter()

# Armazena progresso de missões em memória (em produção, usar Firebase)
mission_progress_storage = {}

def update_character_in_firebase(username: str, character_name: str, updates: dict):
    """Helper para atualizar um personagem no Firebase"""
    personagens_doc = personagens_collection.document(username).get()
    if not personagens_doc.exists:
        return False
    
    personagens_data = personagens_doc.to_dict().get("personagens", [])
    
    # Encontrar e atualizar o personagem
    for idx, char in enumerate(personagens_data):
        if char.get('name') == character_name:
            # Atualizar campos
            for key, value in updates.items():
                if '.' in key:  # Suporta nested keys como "status.hp_atual"
                    keys = key.split('.')
                    current = char
                    for k in keys[:-1]:
                        if k not in current:
                            current[k] = {}
                        current = current[k]
                    current[keys[-1]] = value
                else:
                    char[key] = value
            
            # Salvar de volta no Firebase
            personagens_collection.document(username).update({"personagens": personagens_data})
            return True
    
    return False

@router.get("/missions")
def list_missions(authorization: str = Header(None)):
    """Lista todas as missões disponíveis"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Não autorizado")
    
    try:
        print(f"DEBUG: Authorization header: {authorization[:50]}..." if len(authorization) > 50 else f"DEBUG: Authorization header: {authorization}")
        
        # Remover o prefixo "Bearer " se existir
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        print(f"DEBUG: Token after removing Bearer: {token[:50]}...")
        
        username = verify_key(token)
        print(f"DEBUG: verify_key returned: {username}")
        if not username:
            print("DEBUG: Token validation failed - username is None")
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        print(f"DEBUG: Token validated successfully for user: {username}")
        missions = get_all_missions()
        return {"missions": missions}
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        print(f"ERROR in list_missions: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/missions/start")
def start_mission(request: StartMissionRequest, authorization: str = Header(None)):
    """Inicia uma missão para um personagem"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Não autorizado")
    
    try:
        # Remover o prefixo "Bearer " se existir
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        username = verify_key(token)
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        print(f"DEBUG start_mission: username={username}, character_name={request.character_name}, mission_id={request.mission_id}")
        
        # Buscar personagens do usuário (estrutura correta)
        personagens_doc = personagens_collection.document(username).get()
        if not personagens_doc.exists:
            raise HTTPException(status_code=404, detail="Usuário não possui personagens")
        
        personagens_data = personagens_doc.to_dict().get("personagens", [])
        print(f"DEBUG start_mission: Found {len(personagens_data)} characters")
        
        # Procurar o personagem específico
        character = None
        for char in personagens_data:
            print(f"DEBUG start_mission: Checking character: {char.get('name')}")
            if char.get('name') == request.character_name:
                character = char
                break
        
        if not character:
            char_names = [c.get('name') for c in personagens_data]
            print(f"DEBUG start_mission: Character not found. Available: {char_names}")
            raise HTTPException(status_code=404, detail=f"Personagem '{request.character_name}' não encontrado. Personagens disponíveis: {char_names}")
        
        print(f"DEBUG start_mission: Character found: {character.get('name')}")
        
        # Carregar dados da missão
        mission_data = get_mission(request.mission_id)
        print(f"DEBUG: mission_data type: {type(mission_data)}")
        print(f"DEBUG: mission_data keys: {mission_data.keys() if mission_data else 'None'}")
        
        if not mission_data:
            raise HTTPException(status_code=404, detail="Missão não encontrada")
        
        # Verificar nível mínimo
        if character.get('level', 1) < mission_data['min_level']:
            raise HTTPException(
                status_code=400, 
                detail=f"Nível mínimo necessário: {mission_data['min_level']}"
            )
        
        # Criar cópia da missão para este progresso
        mission_instance = copy.deepcopy(mission_data)
        
        # Inicializar progresso
        progress_key = f"{username}_{request.character_name}_{request.mission_id}"
        mission_progress_storage[progress_key] = {
            "character_name": request.character_name,
            "mission_id": request.mission_id,
            "current_room": mission_instance['starting_room'],
            "visited_rooms": [mission_instance['starting_room']],
            "defeated_enemies": [],
            "collected_treasures": [],
            "completed": False,
            "mission_data": mission_instance
        }
        
        # Marcar sala inicial como visitada
        current_room_id = mission_instance['starting_room']
        print(f"DEBUG: current_room_id: {current_room_id}")
        print(f"DEBUG: rooms keys: {mission_instance['rooms'].keys()}")
        print(f"DEBUG: room type: {type(mission_instance['rooms'][current_room_id])}")
        
        current_room = mission_instance['rooms'][current_room_id]
        current_room['visited'] = True
        
        return {
            "success": True,
            "message": f"Missão '{mission_data['name']}' iniciada!",
            "mission_info": {
                "id": mission_data['id'],
                "name": mission_data['name'],
                "description": mission_data['description'],
                "difficulty": mission_data['difficulty']
            },
            "current_room": {
                "id": current_room['id'],
                "name": current_room['name'],
                "description": current_room['description'],
                "enemies": current_room['enemies'],
                "treasures": current_room['treasures'],
                "exits": current_room['exits']
            },
            "character_status": {
                "hp": character.get('status', {}).get('hp_atual', 100),
                "hp_max": character.get('status', {}).get('hp_max', 100),
                "level": character.get('level', 1),
                "gold": character.get('gold', 0)
            }
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        print(f"ERROR in start_mission: {error_detail}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/missions/action")
def mission_action(request: MissionActionRequest, authorization: str = Header(None)):
    """Executa uma ação durante a missão"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Não autorizado")
    
    try:
        # Remover o prefixo "Bearer " se existir
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        username = verify_key(token)
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        # Buscar progresso da missão
        progress_key = f"{username}_{request.character_name}_{request.mission_id}"
        progress = mission_progress_storage.get(progress_key)
        
        if not progress:
            raise HTTPException(status_code=404, detail="Missão não iniciada ou não encontrada")
        
        if progress['completed']:
            raise HTTPException(status_code=400, detail="Missão já foi completada")
        
        mission_data = progress['mission_data']
        current_room_id = progress['current_room']
        current_room = mission_data['rooms'][current_room_id]
        
        # Buscar personagem (usando estrutura correta)
        personagens_doc = personagens_collection.document(username).get()
        if not personagens_doc.exists:
            raise HTTPException(status_code=404, detail="Usuário não possui personagens")
        
        personagens_data = personagens_doc.to_dict().get("personagens", [])
        character = None
        char_index = None
        for idx, char in enumerate(personagens_data):
            if char.get('name') == request.character_name:
                character = char
                char_index = idx
                break
        
        if not character:
            raise HTTPException(status_code=404, detail="Personagem não encontrado")
        
        result = {
            "success": False,
            "message": "",
            "current_room": {},
            "character_status": {},
            "mission_progress": {}
        }
        
        # AÇÃO: MOVER
        if request.action == "move":
            direction = request.target
            if direction not in current_room['exits']:
                raise HTTPException(status_code=400, detail="Direção inválida")
            
            next_room_id = current_room['exits'][direction]
            
            # Verificar se é o fim da missão
            if next_room_id == "fim":
                # Completar missão e dar recompensas
                rewards = mission_data['rewards']
                character['gold'] = character.get('gold', 0) + rewards.get('gold', 0)
                
                # Atualizar no Firebase
                update_character_in_firebase(username, request.character_name, {"gold": character['gold']})
                
                progress['completed'] = True
                
                result['success'] = True
                result['message'] = f"🎉 Missão completada! Você ganhou {rewards['gold']} de ouro!"
                result['mission_progress'] = {
                    "completed": True,
                    "rewards": rewards
                }
                result['character_status'] = {
                    "hp": character.get('status', {}).get('hp_atual', 100),
                    "hp_max": character.get('status', {}).get('hp_max', 100),
                    "gold": character['gold']
                }
                return result
            
            # Mover para próxima sala
            progress['current_room'] = next_room_id
            if next_room_id not in progress['visited_rooms']:
                progress['visited_rooms'].append(next_room_id)
            
            mission_data['rooms'][next_room_id]['visited'] = True
            next_room = mission_data['rooms'][next_room_id]
            
            result['success'] = True
            result['message'] = f"Você se moveu para: {next_room['name']}"
            result['current_room'] = {
                "id": next_room['id'],
                "name": next_room['name'],
                "description": next_room['description'],
                "enemies": next_room['enemies'],
                "treasures": next_room['treasures'],
                "exits": next_room['exits']
            }
        
        # AÇÃO: LUTAR
        elif request.action == "fight":
            enemy_id = request.target
            enemy = None
            
            for e in current_room['enemies']:
                if e['id'] == enemy_id:
                    enemy = e
                    break
            
            if not enemy:
                raise HTTPException(status_code=400, detail="Inimigo não encontrado nesta sala")
            
            if enemy_id in progress['defeated_enemies']:
                raise HTTPException(status_code=400, detail="Inimigo já foi derrotado")
            
            # Combate simplificado (o frontend pode fazer mais elaborado)
            char_hp = character.get('status', {}).get('hp_atual', 100)
            enemy_hp = enemy['hp']
            
            # Personagem ataca primeiro
            enemy_hp -= 15  # Dano fixo simplificado
            
            if enemy_hp > 0:
                # Inimigo contra-ataca
                char_hp -= enemy['attack']
            
            # Atualizar HP do personagem
            character['status']['hp_atual'] = max(0, char_hp)
            update_character_in_firebase(username, request.character_name, {"status.hp_atual": character['status']['hp_atual']})
            
            if enemy_hp <= 0:
                # Inimigo derrotado
                progress['defeated_enemies'].append(enemy_id)
                character['gold'] = character.get('gold', 0) + enemy.get('gold_drop', 0)
                update_character_in_firebase(username, request.character_name, {"gold": character['gold']})
                
                # Remover inimigo da sala
                current_room['enemies'] = [e for e in current_room['enemies'] if e['id'] != enemy_id]
                
                result['success'] = True
                result['message'] = f"⚔️ Você derrotou {enemy['name']}! Ganhou {enemy.get('gold_drop', 0)} de ouro."
            else:
                result['success'] = True
                result['message'] = f"⚔️ Você atacou {enemy['name']}! O inimigo ainda tem {enemy_hp} HP."
            
            result['current_room'] = {
                "id": current_room['id'],
                "name": current_room['name'],
                "description": current_room['description'],
                "enemies": current_room['enemies'],
                "treasures": current_room['treasures'],
                "exits": current_room['exits']
            }
        
        # AÇÃO: COLETAR
        elif request.action == "collect":
            treasure_id = request.target
            treasure = None
            
            for t in current_room['treasures']:
                if t['id'] == treasure_id:
                    treasure = t
                    break
            
            if not treasure:
                raise HTTPException(status_code=400, detail="Tesouro não encontrado nesta sala")
            
            if treasure_id in progress['collected_treasures']:
                raise HTTPException(status_code=400, detail="Tesouro já foi coletado")
            
            # Coletar tesouro
            progress['collected_treasures'].append(treasure_id)
            contents = treasure.get('contents', {})
            
            gold_gained = contents.get('gold', 0)
            character['gold'] = character.get('gold', 0) + gold_gained
            update_character_in_firebase(username, request.character_name, {"gold": character['gold']})
            
            # Remover tesouro da sala
            current_room['treasures'] = [t for t in current_room['treasures'] if t['id'] != treasure_id]
            
            result['success'] = True
            result['message'] = f"💰 Você coletou {treasure['name']}! Ganhou {gold_gained} de ouro."
            result['current_room'] = {
                "id": current_room['id'],
                "name": current_room['name'],
                "description": current_room['description'],
                "enemies": current_room['enemies'],
                "treasures": current_room['treasures'],
                "exits": current_room['exits']
            }
        
        else:
            raise HTTPException(status_code=400, detail="Ação inválida")
        
        # Atualizar status do personagem
        result['character_status'] = {
            "hp": character.get('status', {}).get('hp_atual', 100),
            "hp_max": character.get('status', {}).get('hp_max', 100),
            "gold": character['gold'],
            "level": character.get('level', 1)
        }
        
        result['mission_progress'] = {
            "visited_rooms": len(progress['visited_rooms']),
            "defeated_enemies": len(progress['defeated_enemies']),
            "collected_treasures": len(progress['collected_treasures']),
            "completed": progress['completed']
        }
        
        return result
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/missions/{mission_id}")
def get_mission_details(mission_id: str, authorization: str = Header(None)):
    """Retorna detalhes de uma missão específica"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Não autorizado")
    
    try:
        # Remover o prefixo "Bearer " se existir
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        username = verify_key(token)
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido ou expirado")
        
        mission_data = get_mission(mission_id)
        
        if not mission_data:
            raise HTTPException(status_code=404, detail="Missão não encontrada")
        
        return {
            "id": mission_data['id'],
            "name": mission_data['name'],
            "description": mission_data['description'],
            "difficulty": mission_data['difficulty'],
            "min_level": mission_data['min_level'],
            "rewards": mission_data['rewards']
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
