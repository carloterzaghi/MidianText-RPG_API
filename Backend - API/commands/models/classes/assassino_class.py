from ._main_classes import MainClasses

class Assassino(MainClasses):
    def __init__(self):
        super().__init__()
        self.hp_max = 15
        self.hp_tmp = 15
        self.strg = 8
        self.mag = 6
        self.spd = 12
        self.luck = 6
        self.defe = 8
        self.mov = 4
        self.habilidades = [
            "Ataque Furtivo: Causa dano extra quando ataca pelas costas",
            "Velocidade Sombria: Pode se mover duas vezes em um turno",
            "Esquiva Ágil: +2 de chance de esquivar ataques"
        ]
        # Itens iniciais da classe
        self.starting_items = {
            "Poção de Cura": 3,
            "Fuga": 2,
            "Adagas Gêmeas": 1
        }
