from ._main_classes import MainClasses

class Soldado(MainClasses):
    def __init__(self):
        super().__init__()
        self.hp_max = 18
        self.hp_tmp = 18
        self.strg = 16
        self.mag = 3
        self.spd = 5
        self.luck = 4
        self.defe = 15
        self.mov = 2
