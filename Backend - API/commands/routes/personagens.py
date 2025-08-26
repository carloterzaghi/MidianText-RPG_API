from fastapi import APIRouter, HTTPException, Header
from commands.database import personagens_collection
from commands.models.user_model import Usuario
from commands.key_manager import verify_key

router = APIRouter()

# Send personagens
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
