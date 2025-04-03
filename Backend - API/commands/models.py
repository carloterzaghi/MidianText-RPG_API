from pydantic import BaseModel

# Modelo Pydantic para Usuário
class Usuario(BaseModel):
    username: str
    password: str

# Classe base para personagens
class Personagem:
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

# Instâncias globais de personagens
jogador = Jogador("Cavaleiro", 100, 15)
inimigo = Inimigo("Goblin", 50, 5)
