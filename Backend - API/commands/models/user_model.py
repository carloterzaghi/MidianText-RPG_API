from pydantic import BaseModel

# Modelo Pydantic para Usuário
class Usuario(BaseModel):
    username: str
    password: str