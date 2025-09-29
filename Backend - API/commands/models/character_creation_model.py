from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import uuid
from .items_table import ItemTable

class CharacterCreationRequest(BaseModel):
    name: str
    character_class: str
    color: str
    
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
    
    @validator('color')
    def validate_color(cls, v):
        valid_colors = ['verde', 'vermelho', 'azul', 'cinza']
        if v not in valid_colors:
            raise ValueError(f'Cor deve ser uma das seguintes: {", ".join(valid_colors)}')
        return v

class CharacterResponse(BaseModel):
    id: str
    name: str
    character_class: str
    level: int
    status: dict
    itens: dict  # Mudado de list para dict
    habilidades: list
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
    def __init__(self, name: str, character_class: str, class_instance, color: str = "cinza"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.character_class = character_class
        self.level = 1
        
        # Aplicar cor escolhida
        class_instance.put_color(color)
        
        self.status = {
            "hp_max": class_instance.hp_max,
            "hp_atual": class_instance.hp_max,
            "strg": class_instance.strg,
            "mag": class_instance.mag,
            "spd": class_instance.spd,
            "luck": class_instance.luck,
            "defe": class_instance.defe,
            "mov": class_instance.mov
        }
        
        # Itens iniciais baseados na classe
        self.itens = getattr(class_instance, 'starting_items', {}).copy()
        
        # Habilidades da classe
        self.habilidades = getattr(class_instance, 'habilidades', [])
        self.color = color  # Cor do personagem
        
        # Manter compatibilidade com sistema antigo
        self.hp_max = class_instance.hp_max
        self.hp_tmp = class_instance.hp_max
        self.strg = class_instance.strg
        self.mag = class_instance.mag
        self.spd = class_instance.spd
        self.luck = class_instance.luck
        self.defe = class_instance.defe
        self.mov = class_instance.mov
        self.created_at = datetime.now().isoformat()
    
    def calculate_damage_multiplier(self, target_color: str) -> float:
        """
        Calcula o multiplicador de dano baseado na vantagem de cor.
        Vermelho > Verde > Azul > Vermelho (como pedra, papel, tesoura)
        Cinza é neutro (sem vantagem nem desvantagem)
        """
        if self.color == "cinza" or target_color == "cinza":
            return 1.0  # Neutro
        
        advantages = {
            "vermelho": "verde",  # Vermelho ganha do verde
            "verde": "azul",      # Verde ganha do azul
            "azul": "vermelho"    # Azul ganha do vermelho
        }
        
        if advantages.get(self.color) == target_color:
            return 1.5  # Vantagem: x1.5 de dano
        elif advantages.get(target_color) == self.color:
            return 0.75  # Desvantagem: reduz dano
        else:
            return 1.0  # Sem vantagem/desvantagem
    
    def get_color_info(self) -> dict:
        """Retorna informações sobre a cor e suas vantagens."""
        color_info = {
            "verde": {
                "name": "🟢 Verde", 
                "advantage": "azul", 
                "disadvantage": "vermelho",
                "description": "Forte contra azul, fraco contra vermelho"
            },
            "vermelho": {
                "name": "🔴 Vermelho", 
                "advantage": "verde", 
                "disadvantage": "azul",
                "description": "Forte contra verde, fraco contra azul"
            },
            "azul": {
                "name": "🔵 Azul", 
                "advantage": "vermelho", 
                "disadvantage": "verde",
                "description": "Forte contra vermelho, fraco contra verde"
            },
            "cinza": {
                "name": "⚫ Cinza", 
                "advantage": "nenhuma", 
                "disadvantage": "nenhuma",
                "description": "Neutro - sem vantagens nem desvantagens"
            }
        }
        return color_info.get(self.color, color_info["cinza"])
    
    def get_detailed_items(self) -> dict:
        """Retorna informações detalhadas dos itens do personagem."""
        detailed_items = {}
        
        for item_name, quantity in self.itens.items():
            item_info = ItemTable.get_item_info(item_name)
            if item_info:
                detailed_items[item_name] = {
                    "quantidade": quantity,
                    "info": item_info
                }
            else:
                detailed_items[item_name] = {
                    "quantidade": quantity,
                    "info": {"tipo": "desconhecido", "descricao": "Item não encontrado"}
                }
        
        return detailed_items
    
    def add_item(self, item_name: str, quantity: int = 1) -> bool:
        """Adiciona um item ao inventário do personagem."""
        if item_name in self.itens:
            self.itens[item_name] += quantity
        else:
            self.itens[item_name] = quantity
        return True
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove um item do inventário do personagem."""
        if item_name not in self.itens:
            return False
        
        if self.itens[item_name] <= quantity:
            del self.itens[item_name]
        else:
            self.itens[item_name] -= quantity
        
        return True
    
    def to_dict(self):
        return {
            "classe": self.character_class,
            "level": self.level,
            "status": self.status,
            "itens": self.itens,
            "habilidades": self.habilidades,
            "color": self.color
        }
    
    def to_dict_full(self):
        """Retorna dicionário completo para compatibilidade"""
        return {
            "id": self.id,
            "name": self.name,
            "character_class": self.character_class,
            "level": self.level,
            "status": self.status,
            "itens": self.itens,
            "habilidades": self.habilidades,
            "color": self.color,
            "hp_max": self.hp_max,
            "hp_tmp": self.hp_tmp,
            "strg": self.strg,
            "mag": self.mag,
            "spd": self.spd,
            "luck": self.luck,
            "defe": self.defe,
            "mov": self.mov,
            "created_at": self.created_at
        }