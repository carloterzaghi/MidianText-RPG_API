from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from commands.routes.login import router as login_router
from commands.routes.personagens import router as personagens_router


app = FastAPI()

# Habilitar CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar as rotas de login e personagens
app.include_router(login_router)
app.include_router(personagens_router)

# Rodar a API
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
