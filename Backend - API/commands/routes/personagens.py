from fastapi import APIRouter, HTTPException
from commands.database import usuarios_collection, personagens_collection
from commands.models.user_model import Usuario

router = APIRouter()

# Send personagens
@router.get("/personagens/{username}", response_model=list)
def get_personagens(username: str) -> list:
    """
    Obtém a lista de personagens associados a um usuário usando Firebase Firestore.
    """

    # Busca o usuário pelo username
    query = usuarios_collection.where("username", "==", username).get()
    if not query:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user_doc = query[0]
    user_id = user_doc.id

    # Busca os personagens pelo user_id
    personagens_doc = personagens_collection.document(user_id).get()
    if not personagens_doc.exists:
        return []

    personagens_data = personagens_doc.to_dict().get("personagens", [])
    
    return personagens_data
