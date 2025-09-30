from fastapi import APIRouter, HTTPException, Header
from commands.database import personagens_collection
from commands.models.user_model import Usuario
from commands.models.character_creation_model import CharacterCreationRequest, CharacterResponse, Character
from commands.key_manager import verify_key
from commands.models.classes.assassino_class import Assassino
from commands.models.classes.arqueiro_class import Arqueiro
from commands.models.classes.mage_class import Mago
from commands.models.classes.soldado_class import Soldado
from commands.models.items_table import ItemTable
from google.cloud import firestore

router = APIRouter()

# Mapeamento das classes disponíveis
CLASS_MAP = {
    "Assassino": Assassino,
    "Arqueiro": Arqueiro, 
    "Mago": Mago,
    "Soldado": Soldado
}

@router.get("/personagens", response_model=list)
def get_personagens(authorization: str = Header(None)) -> list:
    """
    Obtém a lista de personagens associados a um usuário usando Firebase Firestore.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Não autorizado")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Formato de token inválido")
    except ValueError:
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    user_id = verify_key(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    # Busca os personagens pelo user_id
    personagens_doc = personagens_collection.document(user_id).get()
    if not personagens_doc.exists:
        return []

    personagens_data = personagens_doc.to_dict().get("personagens", [])
    
    return personagens_data

@router.post("/personagens/criar", response_model=CharacterResponse)
def criar_personagem(character_data: CharacterCreationRequest, authorization: str = Header(None)):
    """
    Cria um novo personagem para o usuário autenticado.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Não autorizado")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Formato de token inválido")
    except ValueError:
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    user_id = verify_key(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    # Verifica se a classe existe
    if character_data.character_class not in CLASS_MAP:
        raise HTTPException(status_code=400, detail="Classe de personagem inválida")
    
    # Busca os personagens existentes
    personagens_doc = personagens_collection.document(user_id).get()
    personagens_existentes = []
    if personagens_doc.exists:
        personagens_existentes = personagens_doc.to_dict().get("personagens", [])
    
    # Verifica se já existe um personagem com o mesmo nome
    for personagem in personagens_existentes:
        if personagem.get("name", "").lower() == character_data.name.lower():
            raise HTTPException(status_code=400, detail="Já existe um personagem com este nome")
    
    # Verifica limite de personagens (máximo 3 por usuário)
    if len(personagens_existentes) >= 3:
        raise HTTPException(status_code=400, detail="Limite máximo de 3 personagens atingido")
    
    # Cria a instância da classe do personagem
    class_instance = CLASS_MAP[character_data.character_class]()
    
    # Cria o novo personagem
    novo_personagem = Character(
        name=character_data.name,
        character_class=character_data.character_class,
        class_instance=class_instance,
        color=character_data.color
    )
    
    # Adiciona o personagem à lista (formato antigo para compatibilidade)
    personagens_existentes.append(novo_personagem.to_dict_full())
    
    # Salva no Firebase com nova estrutura: nome do personagem como chave
    try:
        # Salvar na estrutura antiga (compatibilidade)
        personagens_collection.document(user_id).set({
            "personagens": personagens_existentes
        })
        
        # Salvar na nova estrutura: nome como chave
        nova_estrutura = personagens_collection.document(user_id).get()
        dados_atuais = nova_estrutura.to_dict() if nova_estrutura.exists else {}
        
        # Adicionar o personagem com nome como chave
        dados_atuais[character_data.name] = novo_personagem.to_dict()
        
        # Atualizar documento com nova estrutura
        personagens_collection.document(user_id).update(dados_atuais)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar personagem: {str(e)}")
    
    return CharacterResponse(**novo_personagem.to_dict_full())

@router.delete("/personagens/{character_name}")
def deletar_personagem(character_name: str, authorization: str = Header(None)):
    """
    Deleta um personagem específico do usuário autenticado.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Não autorizado")

    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Formato de token inválido")
    except ValueError:
        raise HTTPException(status_code=401, detail="Formato de token inválido")

    user_id = verify_key(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    # Busca os personagens existentes
    personagens_doc = personagens_collection.document(user_id).get()
    if not personagens_doc.exists:
        raise HTTPException(status_code=404, detail="Nenhum personagem encontrado")
    
    personagens_existentes = personagens_doc.to_dict().get("personagens", [])
    
    # Procura o personagem para deletar
    personagem_encontrado = False
    personagens_atualizados = []
    
    for personagem in personagens_existentes:
        if personagem.get("name", "").lower() != character_name.lower():
            personagens_atualizados.append(personagem)
        else:
            personagem_encontrado = True
    
    if not personagem_encontrado:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")
    
    try:
        # Atualizar a lista de personagens (estrutura antiga)
        personagens_collection.document(user_id).update({
            "personagens": personagens_atualizados
        })
        
        # Remover da nova estrutura também (nome como chave)
        personagens_collection.document(user_id).update({
            character_name: firestore.DELETE_FIELD
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar personagem: {str(e)}")
    
    return {"message": f"Personagem '{character_name}' deletado com sucesso"}

@router.get("/personagens/classes")
def get_classes_disponiveis():
    """
    Retorna as classes de personagem disponíveis com suas estatísticas base.
    """
    classes_info = {}
    
    for class_name, class_type in CLASS_MAP.items():
        instance = class_type()
        classes_info[class_name] = {
            "name": class_name,
            "stats": {
                "hp_max": instance.hp_max,
                "strg": instance.strg,
                "mag": instance.mag,
                "spd": instance.spd,
                "luck": instance.luck,
                "defe": instance.defe,
                "mov": instance.mov
            },
            "habilidades": getattr(instance, 'habilidades', [])
        }
    
    return classes_info

@router.get("/personagens/cores")
def get_cores_disponiveis():
    """
    Retorna as cores disponíveis e suas vantagens.
    """
    cores_info = {
        "verde": {
            "name": "🟢 Verde",
            "emoji": "🟢",
            "advantage": "azul",
            "disadvantage": "vermelho",
            "description": "Forte contra azul, fraco contra vermelho",
            "damage_bonus": "x1.5 contra azul"
        },
        "vermelho": {
            "name": "🔴 Vermelho",
            "emoji": "🔴",
            "advantage": "verde",
            "disadvantage": "azul", 
            "description": "Forte contra verde, fraco contra azul",
            "damage_bonus": "x1.5 contra verde"
        },
        "azul": {
            "name": "🔵 Azul",
            "emoji": "🔵",
            "advantage": "vermelho",
            "disadvantage": "verde",
            "description": "Forte contra vermelho, fraco contra verde",
            "damage_bonus": "x1.5 contra vermelho"
        },
        "cinza": {
            "name": "⚫ Cinza",
            "emoji": "⚫",
            "advantage": "nenhuma",
            "disadvantage": "nenhuma",
            "description": "Neutro - sem vantagens nem desvantagens",
            "damage_bonus": "sem bônus"
        }
    }
    
    return {
        "cores": cores_info,
        "sistema": {
            "description": "Sistema de vantagens como Pedra, Papel, Tesoura",
            "regras": [
                "Vermelho vence Verde (x1.5 dano)",
                "Verde vence Azul (x1.5 dano)", 
                "Azul vence Vermelho (x1.5 dano)",
                "Cinza é neutro (sem bônus/penalidade)"
            ]
        }
    }

@router.get("/personagens/itens")
def get_itens_disponiveis():
    """
    Retorna informações sobre todos os itens do jogo.
    """
    return ItemTable.get_items_summary()

@router.get("/personagens/itens/{item_name}")
def get_item_info(item_name: str):
    """
    Retorna informações detalhadas sobre um item específico.
    """
    item_info = ItemTable.get_item_info(item_name)
    if not item_info:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    return {
        "nome": item_name,
        "informacoes": item_info
    }

@router.get("/personagens/itens/classe/{character_class}")
def get_starting_items_for_class(character_class: str):
    """
    Retorna os itens iniciais para uma classe específica.
    """
    valid_classes = ['Assassino', 'Arqueiro', 'Mago', 'Soldado']
    if character_class not in valid_classes:
        raise HTTPException(status_code=400, detail="Classe inválida")
    
    starting_items = ItemTable.get_starting_items(character_class)
    detailed_items = {}
    
    for item_name, quantity in starting_items.items():
        item_info = ItemTable.get_item_info(item_name)
        detailed_items[item_name] = {
            "quantidade": quantity,
            "info": item_info
        }
    
    return {
        "classe": character_class,
        "itens_iniciais": detailed_items
    }
