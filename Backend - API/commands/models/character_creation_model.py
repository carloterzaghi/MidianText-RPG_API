from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import uuid

class CharacterCreationRequest(BaseModel):
    name: str
    character_class: str
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 caracteres')
        if len(v.strip()) > 20:
            raise ValueError('Nome deve ter no máximo 20 caracteres')
        return v.strip()
    
    @validator('character_class')
    def validate_character_class(cls, v):
        valid_classes = ['Assassino', 'Arqueiro', 'Mago', 'Soldado']
        if v not in valid_classes:
            raise ValueError(f'Classe deve ser uma das seguintes: {", ".join(valid_classes)}')
        return v

class CharacterResponse(BaseModel):
    id: str
    name: str
    character_class: str
    level: int
    hp_max: int
    hp_tmp: int
    strg: int
    mag: int
    spd: int
    luck: int
    defe: int
    mov: int
    color: Optional[str]
    created_at: str
    
class Character:
    def __init__(self, name: str, character_class: str, class_instance):
        self.id = str(uuid.uuid4())
        self.name = name
        self.character_class = character_class
        self.level = 1
        self.hp_max = class_instance.hp_max
        self.hp_tmp = class_instance.hp_tmp
        self.strg = class_instance.strg
        self.mag = class_instance.mag
        self.spd = class_instance.spd
        self.luck = class_instance.luck
        self.defe = class_instance.defe
        self.mov = class_instance.mov
        self.color = class_instance.color
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "character_class": self.character_class,
            "level": self.level,
            "hp_max": self.hp_max,
            "hp_tmp": self.hp_tmp,
            "strg": self.strg,
            "mag": self.mag,
            "spd": self.spd,
            "luck": self.luck,
            "defe": self.defe,
            "mov": self.mov,
            "color": self.color,
            "created_at": self.created_at
        }