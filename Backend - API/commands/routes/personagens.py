from fastapi import APIRouter, HTTPException
from commands.database import usuarios_collection,personagens_collection
from commands.models.user_model import Usuario

router = APIRouter()

# Send personagens
@router.get("/personagens/{username}", response_model=list)
def get_personagens(username: str) -> list:
    """
    Obtém a lista de personagens associados a um usuário.

    Esta rota busca no banco de dados a coleção de personagens de um usuário específico.
    Se o usuário existir mas não tiver personagens cadastrados, retorna uma lista vazia.
    Se o usuário não for encontrado, retorna um erro 404.

    Parâmetros:
        username (str): Nome de usuário do qual se deseja obter os personagens.

    Retorna:
        list: Lista contendo os personagens do usuário. Caso o usuário não possua 
              personagens cadastrados, retorna uma lista vazia.

    Erros:
        404 - Usuário não encontrado.
    """
    
    usuario = usuarios_collection.find_one({"username": username})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    personagens = personagens_collection.find_one({"user_id": usuario["_id"]})

    # Se `personagens` for None, retorna uma lista vazia
    return personagens["personagens"]
