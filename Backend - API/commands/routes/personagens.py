from fastapi import APIRouter, HTTPException, Header
from commands.database import personagens_collection
from commands.models.user_model import Usuario
from commands.models.character_creation_model import CharacterCreationRequest, CharacterResponse, Character
from commands.key_manager import verify_key
from commands.models.classes.assassino_class import Assassino
from commands.models.classes.arqueiro_class import Arqueiro
from commands.models.classes.mage_class import Mago
from commands.models.classes.soldado_class import Soldado

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
    
    # Verifica limite de personagens (máximo 5 por usuário)
    if len(personagens_existentes) >= 5:
        raise HTTPException(status_code=400, detail="Limite máximo de 5 personagens atingido")
    
    # Cria a instância da classe do personagem
    class_instance = CLASS_MAP[character_data.character_class]()
    
    # Cria o novo personagem
    novo_personagem = Character(
        name=character_data.name,
        character_class=character_data.character_class,
        class_instance=class_instance
    )
    
    # Adiciona o personagem à lista
    personagens_existentes.append(novo_personagem.to_dict())
    
    # Salva no Firebase
    try:
        personagens_collection.document(user_id).set({
            "personagens": personagens_existentes
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar personagem: {str(e)}")
    
    return CharacterResponse(**novo_personagem.to_dict())

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
            }
        }
    
    return classes_info
