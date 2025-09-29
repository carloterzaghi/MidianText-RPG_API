# Tabela de Itens do Jogo
from typing import Dict, Any

class ItemTable:
    """
    Catálogo centralizado de todos os itens existentes no sistema.
    Este arquivo serve apenas como referência de todos os itens disponíveis.
    Os itens iniciais de cada classe estão definidos nos respectivos arquivos de classe.
    """
    
    # Catálogo completo de itens do jogo
    ALL_ITEMS = {
        # Itens Consumíveis
        "Poção de Cura": {
            "tipo": "consumivel",
            "efeito": "Restaura 25 HP",
            "descricao": "Uma poção mágica que cura ferimentos menores",
            "emoji": "🧪",
            "valor": 50
        },
        "Fuga": {
            "tipo": "consumivel", 
            "efeito": "Permite escapar de qualquer combate",
            "descricao": "Pergaminho mágico que permite fuga instantânea",
            "emoji": "📜",
            "valor": 100
        },
        
        # Armas de Assassino
        "Adagas Gêmeas": {
            "tipo": "arma",
            "efeito": "+3 Velocidade, +2 Sorte em combate",
            "descricao": "Par de adagas afiadas e equilibradas, perfeitas para ataques rápidos",
            "emoji": "🗡️",
            "valor": 300,
            "classe": "Assassino"
        },
        
        # Armas de Arqueiro
        "Arco Élfico": {
            "tipo": "arma",
            "efeito": "+4 Força, +2 Velocidade em combate",
            "descricao": "Arco feito de madeira élfica, aumenta precisão e alcance",
            "emoji": "🏹",
            "valor": 350,
            "classe": "Arqueiro"
        },
        
        # Armas de Mago
        "Cajado Arcano": {
            "tipo": "arma",
            "efeito": "+5 Magia, +1 Defesa mágica",
            "descricao": "Cajado imbuído com cristais mágicos, amplifica poderes arcanos",
            "emoji": "🔮",
            "valor": 400,
            "classe": "Mago"
        },
        
        # Armaduras de Soldado
        "Escudo de Ferro": {
            "tipo": "armadura",
            "efeito": "+4 Defesa, +2 HP máximo",
            "descricao": "Escudo robusto forjado em ferro, oferece proteção superior",
            "emoji": "🛡️",
            "valor": 250,
            "classe": "Soldado"
        }
    }
    
    @classmethod 
    def get_starting_items(cls, character_class: str) -> Dict[str, int]:
        """
        Retorna os itens iniciais para uma classe específica.
        NOTA: Este método agora busca os itens diretamente da instância da classe.
        
        Args:
            character_class: Nome da classe do personagem
            
        Returns:
            Dicionário com nome do item como chave e quantidade como valor
        """
        # Importar as classes aqui para evitar import circular
        from .classes.assassino_class import Assassino
        from .classes.arqueiro_class import Arqueiro
        from .classes.mage_class import Mago
        from .classes.soldado_class import Soldado
        
        class_map = {
            "Assassino": Assassino,
            "Arqueiro": Arqueiro,
            "Mago": Mago,
            "Soldado": Soldado
        }
        
        if character_class in class_map:
            instance = class_map[character_class]()
            return getattr(instance, 'starting_items', {})
        
        return {}
    
    @classmethod
    def get_item_info(cls, item_name: str) -> Dict[str, Any]:
        """
        Retorna informações detalhadas sobre um item.
        
        Args:
            item_name: Nome do item
            
        Returns:
            Dicionário com informações do item ou None se não encontrado
        """
        return cls.ALL_ITEMS.get(item_name)
    
    @classmethod
    def get_all_items_by_type(cls, item_type: str) -> Dict[str, Dict[str, Any]]:
        """
        Retorna todos os itens de um tipo específico.
        
        Args:
            item_type: Tipo do item (arma, armadura, consumivel)
            
        Returns:
            Dicionário com itens do tipo especificado
        """
        return {
            name: info for name, info in cls.ALL_ITEMS.items() 
            if info.get("tipo") == item_type
        }
    
    @classmethod
    def get_all_items_by_class(cls, character_class: str) -> Dict[str, Dict[str, Any]]:
        """
        Retorna todos os itens específicos de uma classe.
        
        Args:
            character_class: Nome da classe
            
        Returns:
            Dicionário com itens da classe especificada
        """
        return {
            name: info for name, info in cls.ALL_ITEMS.items() 
            if info.get("classe") == character_class
        }
    
    @classmethod
    def get_items_summary(cls) -> Dict[str, Any]:
        """
        Retorna um resumo de todos os itens organizados por categoria.
        
        Returns:
            Dicionário organizado com itens por categoria
        """
        consumiveis = cls.get_all_items_by_type("consumivel")
        armas = cls.get_all_items_by_type("arma")
        armaduras = cls.get_all_items_by_type("armadura")
        
        summary = {
            "total_itens": len(cls.ALL_ITEMS),
            "consumiveis": consumiveis,
            "armas": armas,
            "armaduras": armaduras,
            "tipos_disponiveis": list(set(
                item.get("tipo", "indefinido") 
                for item in cls.ALL_ITEMS.values()
            )),
            "classes_com_itens": list(set(
                item.get("classe", "comum") 
                for item in cls.ALL_ITEMS.values()
                if item.get("classe")
            ))
        }
        
        return summary