from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
import bcrypt
import uvicorn

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MidiaText"]
usuarios_collection = db["usuarios"]

app = FastAPI()

# Habilitar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo Pydantic para Usuário
class Usuario(BaseModel):
    username: str
    password: str

# Função para hash de senha
def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return bcrypt.checkpw(senha.encode('utf-8'), hash_senha.encode('utf-8'))

# Endpoint de Registro
@app.post("/register")
async def register(usuario: Usuario):
    if usuarios_collection.find_one({"username": usuario.username}):
        raise HTTPException(status_code=400, detail="Nome de usuário já existe!")
    
    senha_hash = hash_senha(usuario.password)
    usuarios_collection.insert_one({"username": usuario.username, "password": senha_hash})
    return {"message": "Usuário registrado com sucesso"}

# Endpoint de Login
@app.post("/login")
async def login(usuario: Usuario):
    user = usuarios_collection.find_one({"username": usuario.username})
    if not user or not verificar_senha(usuario.password, user['password']):
        raise HTTPException(status_code=401, detail="Usuário ou Senha inválida!")
    
    return {"message": "Login bem-sucedido"}

# Classe base para personagens
class Personagem():
    def __init__(self, nome: str, vida: int, ataque: int):
        self.nome = nome
        self.vida = vida
        self.ataque = ataque
    
    def atacar(self, inimigo):
        inimigo.vida -= self.ataque
        return f"{self.nome} atacou {inimigo.nome} causando {self.ataque} de dano!"

# Classe Jogador
class Jogador(Personagem):
    def __init__(self, nome: str, vida: int, ataque: int, nivel: int = 1):
        super().__init__(nome, vida, ataque)
        self.nivel = nivel

# Classe Inimigo
class Inimigo(Personagem):
    def __init__(self, nome: str, vida: int, ataque: int):
        super().__init__(nome, vida, ataque)

# Exemplo de instância de jogador e inimigo
jogador = Jogador("Cavaleiro", 100, 15)
inimigo = Inimigo("Goblin", 50, 5)

@app.get("/batalha")
async def batalha():
    resultado = jogador.atacar(inimigo)
    return {"batalha": resultado, "vida_inimigo": inimigo.vida}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
