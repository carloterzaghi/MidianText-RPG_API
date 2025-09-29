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
