from ._main_classes import MainClasses

class Mago(MainClasses):
    def __init__(self):
        super().__init__()
        self.hp_max = 11
        self.hp_tmp = 11
        self.strg = 3
        self.mag = 18
        self.spd = 7
        self.luck = 5
        self.defe = 6
        self.mov = 3
        self.habilidades = [
            "Bola de Fogo: Ataque mágico de fogo em área",
            "Cura Menor: Restaura HP próprio ou de aliados",
            "Escudo Mágico: Aumenta defesa temporariamente",
            "Raio Gélido: Ataque que reduz velocidade do inimigo"
        ]
        # Itens iniciais da classe
        self.starting_items = {
            "Poção de Cura": 3,
            "Fuga": 2,
            "Cajado Arcano": 1
        }
