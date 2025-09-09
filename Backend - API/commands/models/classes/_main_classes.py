class MainClasses():
    def __init__(self):
        self.hp_max = 0
        self.hp_tmp = 0
        self.lv = 1
        self.strg = 0
        self.mag = 0
        self.spd = 0
        self.luck = 0
        self.defe = 0
        self.mov = 0
        self.color = None
    
    def get_status(self):
        return {
            "hp_max": self.hp_max,
            "hp_tmp": self.hp_tmp ,
            "lv": self.lv,
            "strg": self.strg,
            "mag": self.mag,
            "spd": self.spd,
            "luck": self.luck,
            "defe": self.defe,
            "mov": self.mov,
            "color": self.color
        }
    
    def put_color(self, color):
        if color in ["green", "red", "blue", "gray"]:
            self.color = color
            return True  # retorna sucesso
        return False  # retorna falha se o status não existir


    def put_status(self, status, number):
        if status in ["hp_max", "hp_tmp", "lv", "strg", "mag", "spd", "luck", "defe", "mov"]:
            setattr(self, status, number)
            return True  # retorna sucesso
        return False  # retorna falha se o status não existir

    def add_status(self, status, number):
        if status in ["hp_max", "hp_tmp", "lv", "strg", "mag", "spd", "luck", "defe", "mov"]:
            current = getattr(self, status)
            if current is None:
                current = 0
            setattr(self, status, current + number)
            return True
        return False

    def sub_status(self, status, number):
        if status in ["hp_max", "hp_tmp", "lv", "strg", "mag", "spd", "luck", "defe", "mov"]:
            current = getattr(self, status)
            if current is None:
                current = 0
            setattr(self, status, current - number)
            return True
        return False