import customtkinter as ctk
from typing import Dict, Any, Optional
import api_client

class ShopWindow(ctk.CTkToplevel):
    """Janela da loja do jogo com sistema de compra e venda de itens."""
    
    # Catálogo de itens disponíveis na loja (baseado em items_table.py)
    SHOP_ITEMS = {
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
        "Adagas Gêmeas": {
            "tipo": "arma",
            "efeito": "+3 Velocidade, +2 Sorte em combate",
            "descricao": "Par de adagas afiadas e equilibradas, perfeitas para ataques rápidos",
            "emoji": "🗡️",
            "valor": 300,
            "classe": "Assassino"
        },
        "Arco Élfico": {
            "tipo": "arma",
            "efeito": "+4 Força, +2 Velocidade em combate",
            "descricao": "Arco feito de madeira élfica, aumenta precisão e alcance",
            "emoji": "🏹",
            "valor": 350,
            "classe": "Arqueiro"
        },
        "Cajado Arcano": {
            "tipo": "arma",
            "efeito": "+5 Magia, +1 Defesa mágica",
            "descricao": "Cajado imbuído com cristais mágicos, amplifica poderes arcanos",
            "emoji": "🔮",
            "valor": 400,
            "classe": "Mago"
        },
        "Escudo de Ferro": {
            "tipo": "armadura",
            "efeito": "+4 Defesa, +2 HP máximo",
            "descricao": "Escudo robusto forjado em ferro, oferece proteção superior",
            "emoji": "🛡️",
            "valor": 250,
            "classe": "Soldado"
        },
        "Poção Grande de Cura": {
            "tipo": "consumivel",
            "efeito": "Restaura 50 HP",
            "descricao": "Poção mágica poderosa que cura ferimentos graves",
            "emoji": "🧪",
            "valor": 120
        },
        "Elixir de Força": {
            "tipo": "consumivel",
            "efeito": "+5 Força temporária (1 combate)",
            "descricao": "Elixir que aumenta temporariamente a força física",
            "emoji": "💪",
            "valor": 80
        },
        "Elixir de Magia": {
            "tipo": "consumivel",
            "efeito": "+5 Magia temporária (1 combate)",
            "descricao": "Elixir que amplifica temporariamente poderes mágicos",
            "emoji": "✨",
            "valor": 80
        }
    }
    
    def __init__(self, parent, controller, character):
        """
        Inicializa a janela da loja.
        
        Args:
            parent: Widget pai
            controller: Controlador principal da aplicação
            character: Dados do personagem atual
        """
        super().__init__(parent)
        
        self.controller = controller
        self.character = character
        self.current_filter = "Todos"  # Filtro atual
        
        # Configurar janela
        self.title("🛍️ Loja - Midian Text RPG")
        self.geometry("1000x700")
        self.transient(parent)
        self.grab_set()
        
        # Centralizar janela
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.winfo_screenheight() // 2) - (700 // 2)
        self.geometry(f"1000x700+{x}+{y}")
        
        # Criar interface
        self.create_ui()
        
        # Atualizar dados do personagem
        self.refresh_character_data()
    
    def create_ui(self):
        """Cria a interface da loja."""
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header(main_frame)
        
        # Área de conteúdo dividida em duas colunas
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, pady=10)
        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=2)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Coluna esquerda - Itens da loja
        self.create_shop_section(content_frame)
        
        # Coluna direita - Inventário do jogador
        self.create_inventory_section(content_frame)
    
    def create_header(self, parent):
        """Cria o cabeçalho da loja."""
        header_frame = ctk.CTkFrame(parent, fg_color=("#868686", "#1a1a1a"))
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Título e informações do personagem
        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=15)
        
        # Título
        title_label = ctk.CTkLabel(
            info_frame,
            text="🛍️ Loja de Midian",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left")
        
        # Informações do personagem
        char_name = self.character.get('name', 'Personagem')
        self.gold_label = ctk.CTkLabel(
            info_frame,
            text=f"💰 {char_name} | Ouro: {self.get_character_gold()}",
            font=ctk.CTkFont(size=16)
        )
        self.gold_label.pack(side="right", padx=20)
        
        # Botão fechar
        close_btn = ctk.CTkButton(
            info_frame,
            text="❌ Fechar",
            command=self.destroy,
            width=100,
            height=30,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        close_btn.pack(side="right")
    
    def create_shop_section(self, parent):
        """Cria a seção de itens da loja."""
        shop_frame = ctk.CTkFrame(parent)
        shop_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Header da seção
        header = ctk.CTkFrame(shop_frame)
        header.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            header,
            text="🏪 Itens Disponíveis",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(side="left")
        
        # Filtros
        filter_frame = ctk.CTkFrame(header, fg_color="transparent")
        filter_frame.pack(side="right")
        
        ctk.CTkLabel(filter_frame, text="Filtrar:", font=ctk.CTkFont(size=12)).pack(side="left", padx=5)
        
        filter_var = ctk.StringVar(value="Todos")
        filter_options = ["Todos", "Consumível", "Arma", "Armadura"]
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            values=filter_options,
            variable=filter_var,
            command=self.apply_filter,
            width=120
        )
        filter_menu.pack(side="left", padx=5)
        
        # Lista de itens com scroll
        self.shop_scroll = ctk.CTkScrollableFrame(shop_frame, label_text="")
        self.shop_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Carregar itens
        self.load_shop_items()
    
    def create_inventory_section(self, parent):
        """Cria a seção de inventário do jogador."""
        inventory_frame = ctk.CTkFrame(parent)
        inventory_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Header da seção
        header = ctk.CTkFrame(inventory_frame)
        header.pack(fill="x", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            header,
            text="🎒 Seu Inventário",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(side="left")
        
        # Botão atualizar
        refresh_btn = ctk.CTkButton(
            header,
            text="🔄",
            command=self.refresh_inventory,
            width=30,
            height=30
        )
        refresh_btn.pack(side="right")
        
        # Lista de itens do inventário com scroll
        self.inventory_scroll = ctk.CTkScrollableFrame(inventory_frame, label_text="")
        self.inventory_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Carregar inventário
        self.load_inventory()
    
    def load_shop_items(self, filter_type: str = "Todos"):
        """
        Carrega os itens da loja.
        
        Args:
            filter_type: Tipo de filtro a aplicar
        """
        # Limpar itens existentes
        for widget in self.shop_scroll.winfo_children():
            widget.destroy()
        
        # Filtrar itens
        filtered_items = self.filter_items(filter_type)
        
        if not filtered_items:
            no_items_label = ctk.CTkLabel(
                self.shop_scroll,
                text="Nenhum item encontrado com este filtro",
                font=ctk.CTkFont(size=14),
                text_color="gray"
            )
            no_items_label.pack(pady=20)
            return
        
        # Criar card para cada item
        for item_name, item_data in filtered_items.items():
            self.create_shop_item_card(item_name, item_data)
    
    def filter_items(self, filter_type: str) -> Dict[str, Any]:
        """
        Filtra itens por tipo.
        
        Args:
            filter_type: Tipo de filtro
            
        Returns:
            Dicionário com itens filtrados
        """
        if filter_type == "Todos":
            return self.SHOP_ITEMS
        
        # Mapear nome do filtro para tipo do item
        type_map = {
            "Consumível": "consumivel",
            "Arma": "arma",
            "Armadura": "armadura"
        }
        
        item_type = type_map.get(filter_type)
        if not item_type:
            return self.SHOP_ITEMS
        
        return {
            name: data for name, data in self.SHOP_ITEMS.items()
            if data.get("tipo") == item_type
        }
    
    def create_shop_item_card(self, item_name: str, item_data: Dict[str, Any]):
        """
        Cria um card de item na loja.
        
        Args:
            item_name: Nome do item
            item_data: Dados do item
        """
        card = ctk.CTkFrame(self.shop_scroll, fg_color=("#f0f0f0", "#2e2e2e"), corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)
        
        # Linha 1: Emoji e Nome
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))
        
        emoji_label = ctk.CTkLabel(
            header_frame,
            text=item_data.get("emoji", "📦"),
            font=ctk.CTkFont(size=24)
        )
        emoji_label.pack(side="left", padx=(0, 10))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=item_name,
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        # Tipo do item
        tipo_badge = ctk.CTkLabel(
            header_frame,
            text=item_data.get("tipo", "item").upper(),
            font=ctk.CTkFont(size=9),
            fg_color=self.get_type_color(item_data.get("tipo")),
            corner_radius=5,
            padx=8,
            pady=2
        )
        tipo_badge.pack(side="right")
        
        # Linha 2: Descrição
        desc_label = ctk.CTkLabel(
            card,
            text=item_data.get("descricao", ""),
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w",
            wraplength=400
        )
        desc_label.pack(fill="x", padx=15, pady=(0, 5))
        
        # Linha 3: Efeito
        effect_label = ctk.CTkLabel(
            card,
            text=f"✨ {item_data.get('efeito', 'Sem efeito')}",
            font=ctk.CTkFont(size=10),
            anchor="w"
        )
        effect_label.pack(fill="x", padx=15, pady=(0, 5))
        
        # Linha 4: Restrição de classe (se houver)
        if "classe" in item_data:
            class_label = ctk.CTkLabel(
                card,
                text=f"⚔️ Exclusivo: {item_data['classe']}",
                font=ctk.CTkFont(size=10),
                text_color="#ff9800",
                anchor="w"
            )
            class_label.pack(fill="x", padx=15, pady=(0, 5))
        
        # Linha 5: Preço e botão comprar
        footer_frame = ctk.CTkFrame(card, fg_color="transparent")
        footer_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        price_label = ctk.CTkLabel(
            footer_frame,
            text=f"💰 {item_data.get('valor', 0)} ouro",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffd700"
        )
        price_label.pack(side="left")
        
        buy_btn = ctk.CTkButton(
            footer_frame,
            text="🛒 Comprar",
            command=lambda: self.buy_item(item_name, item_data),
            width=100,
            height=30,
            fg_color="#28a745",
            hover_color="#1e7e34"
        )
        buy_btn.pack(side="right")
    
    def load_inventory(self):
        """Carrega o inventário do personagem."""
        # Limpar inventário existente
        for widget in self.inventory_scroll.winfo_children():
            widget.destroy()
        
        # Obter itens do personagem
        items = self.character.get('itens', {})
        
        if not items or all(qty == 0 for qty in items.values()):
            empty_label = ctk.CTkLabel(
                self.inventory_scroll,
                text="🎒 Inventário vazio\n\nCompre itens na loja!",
                font=ctk.CTkFont(size=14),
                text_color="gray",
                justify="center"
            )
            empty_label.pack(pady=40)
            return
        
        # Criar card para cada item do inventário
        for item_name, quantity in items.items():
            if quantity > 0:  # Só mostrar itens que o jogador possui
                item_data = self.SHOP_ITEMS.get(item_name)
                if item_data:
                    self.create_inventory_item_card(item_name, quantity, item_data)
    
    def create_inventory_item_card(self, item_name: str, quantity: int, item_data: Dict[str, Any]):
        """
        Cria um card de item no inventário.
        
        Args:
            item_name: Nome do item
            quantity: Quantidade do item
            item_data: Dados do item
        """
        card = ctk.CTkFrame(self.inventory_scroll, fg_color=("#e8f5e9", "#1b5e20"), corner_radius=10)
        card.pack(fill="x", padx=5, pady=5)
        
        # Header
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(8, 3))
        
        emoji_label = ctk.CTkLabel(
            header_frame,
            text=item_data.get("emoji", "📦"),
            font=ctk.CTkFont(size=20)
        )
        emoji_label.pack(side="left", padx=(0, 8))
        
        name_label = ctk.CTkLabel(
            header_frame,
            text=item_name,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        qty_label = ctk.CTkLabel(
            header_frame,
            text=f"x{quantity}",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=("#4caf50", "#2e7d32"),
            corner_radius=5,
            padx=8,
            pady=2
        )
        qty_label.pack(side="right")
        
        # Valor de venda (50% do preço original)
        sell_price = item_data.get('valor', 0) // 2
        
        footer_frame = ctk.CTkFrame(card, fg_color="transparent")
        footer_frame.pack(fill="x", padx=10, pady=(3, 8))
        
        price_label = ctk.CTkLabel(
            footer_frame,
            text=f"💰 Vender: {sell_price} ouro",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        price_label.pack(side="left")
        
        sell_btn = ctk.CTkButton(
            footer_frame,
            text="💸 Vender",
            command=lambda: self.sell_item(item_name, item_data),
            width=80,
            height=25,
            fg_color="#ff9800",
            hover_color="#f57c00",
            font=ctk.CTkFont(size=10)
        )
        sell_btn.pack(side="right")
    
    def buy_item(self, item_name: str, item_data: Dict[str, Any]):
        """
        Compra um item da loja.
        
        Args:
            item_name: Nome do item
            item_data: Dados do item
        """
        price = item_data.get('valor', 0)
        current_gold = self.get_character_gold()
        
        # Verificar se tem ouro suficiente
        if current_gold < price:
            self.show_message_dialog(
                "Ouro Insuficiente",
                f"❌ Você precisa de {price} ouro para comprar {item_name}.\n\nVocê tem apenas {current_gold} ouro.",
                "error"
            )
            return
        
        # Verificar restrição de classe
        required_class = item_data.get('classe')
        char_class = self.character.get('character_class')
        
        if required_class and required_class != char_class:
            self.show_message_dialog(
                "Restrição de Classe",
                f"⚠️ Este item é exclusivo para a classe {required_class}.\n\nSua classe: {char_class}",
                "warning"
            )
            return
        
        # Confirmar compra
        if self.confirm_dialog(
            "Confirmar Compra",
            f"🛒 Deseja comprar {item_name}?\n\n💰 Preço: {price} ouro\n💼 Saldo após compra: {current_gold - price} ouro"
        ):
            # Fazer requisição ao backend
            token = self.controller.access_token
            char_name = self.character.get('name')
            
            result = api_client.buy_item(token, char_name, item_name, quantity=1)
            
            if result and not result.get('error') and result.get('success'):
                # Atualizar dados locais do personagem
                self.character['gold'] = result.get('gold_remaining', current_gold - price)
                self.character['itens'] = result.get('inventory', self.character.get('itens', {}))
                
                # Atualizar interface
                self.refresh_all()
                
                # Mostrar mensagem de sucesso
                self.show_message_dialog(
                    "Compra Realizada",
                    f"✅ Você comprou {item_name}!\n\n{item_data.get('emoji', '📦')} {item_data.get('descricao', '')}",
                    "success"
                )
            else:
                # Mostrar erro
                error_msg = result.get('detail') or result.get('error') or 'Erro ao processar compra'
                self.show_message_dialog(
                    "Erro na Compra",
                    f"❌ {error_msg}",
                    "error"
                )
    
    def sell_item(self, item_name: str, item_data: Dict[str, Any]):
        """
        Vende um item do inventário.
        
        Args:
            item_name: Nome do item
            item_data: Dados do item
        """
        sell_price = item_data.get('valor', 0) // 2  # 50% do valor
        
        # Confirmar venda
        if self.confirm_dialog(
            "Confirmar Venda",
            f"💸 Deseja vender {item_name}?\n\n💰 Você receberá: {sell_price} ouro"
        ):
            # Fazer requisição ao backend
            token = self.controller.access_token
            char_name = self.character.get('name')
            
            result = api_client.sell_item(token, char_name, item_name, quantity=1)
            
            if result and not result.get('error') and result.get('success'):
                # Atualizar dados locais do personagem
                current_gold = self.get_character_gold()
                self.character['gold'] = result.get('gold_total', current_gold + sell_price)
                self.character['itens'] = result.get('inventory', self.character.get('itens', {}))
                
                # Atualizar interface
                self.refresh_all()
                
                # Mostrar mensagem de sucesso
                self.show_message_dialog(
                    "Venda Realizada",
                    f"✅ Você vendeu {item_name} por {sell_price} ouro!",
                    "success"
                )
            else:
                # Mostrar erro
                error_msg = result.get('detail') or result.get('error') or 'Erro ao processar venda'
                self.show_message_dialog(
                    "Erro na Venda",
                    f"❌ {error_msg}",
                    "error"
                )
    
    def apply_filter(self, filter_type: str):
        """
        Aplica filtro aos itens da loja.
        
        Args:
            filter_type: Tipo de filtro selecionado
        """
        self.current_filter = filter_type
        self.load_shop_items(filter_type)
    
    def refresh_all(self):
        """Atualiza toda a interface da loja."""
        self.load_shop_items(self.current_filter)
        self.load_inventory()
        self.update_gold_display()
    
    def refresh_inventory(self):
        """Atualiza apenas o inventário."""
        self.load_inventory()
    
    def refresh_character_data(self):
        """Atualiza os dados do personagem do backend (placeholder)."""
        # TODO: Implementar chamada à API para obter dados atualizados
        # Por enquanto, usa dados locais
        pass
    
    def update_gold_display(self):
        """Atualiza a exibição de ouro no header."""
        char_name = self.character.get('name', 'Personagem')
        self.gold_label.configure(text=f"💰 {char_name} | Ouro: {self.get_character_gold()}")
    
    def get_character_gold(self) -> int:
        """
        Obtém o ouro atual do personagem.
        
        Returns:
            Quantidade de ouro
        """
        # Tenta obter do backend primeiro
        gold = self.character.get('gold', None)
        
        # Se não existir no objeto (personagens antigos), usa valor padrão
        if gold is None:
            gold = 1000  # Valor padrão para personagens antigos
            self.character['gold'] = gold
        
        return gold
    
    def get_type_color(self, item_type: str) -> str:
        """
        Retorna a cor do badge baseado no tipo.
        
        Args:
            item_type: Tipo do item
            
        Returns:
            Código de cor
        """
        colors = {
            "consumivel": "#4caf50",
            "arma": "#f44336",
            "armadura": "#2196f3"
        }
        return colors.get(item_type, "#9e9e9e")
    
    def show_message_dialog(self, title: str, message: str, msg_type: str = "info"):
        """
        Mostra um diálogo de mensagem.
        
        Args:
            title: Título do diálogo
            message: Mensagem a exibir
            msg_type: Tipo da mensagem (info, success, error, warning)
        """
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"400x250+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ícone baseado no tipo
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "error": "❌",
            "warning": "⚠️"
        }
        icon = icons.get(msg_type, "ℹ️")
        
        icon_label = ctk.CTkLabel(main_frame, text=icon, font=ctk.CTkFont(size=36))
        icon_label.pack(pady=(10, 10))
        
        # Mensagem
        msg_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=350,
            justify="center"
        )
        msg_label.pack(pady=10)
        
        # Botão OK
        ok_btn = ctk.CTkButton(main_frame, text="OK", command=dialog.destroy, width=100)
        ok_btn.pack(pady=15)
    
    def confirm_dialog(self, title: str, message: str) -> bool:
        """
        Mostra um diálogo de confirmação.
        
        Args:
            title: Título do diálogo
            message: Mensagem a exibir
            
        Returns:
            True se confirmado, False caso contrário
        """
        result = [False]  # Lista para armazenar o resultado
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("450x280")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (280 // 2)
        dialog.geometry(f"450x280+{x}+{y}")
        
        def on_confirm():
            result[0] = True
            dialog.destroy()
        
        def on_cancel():
            result[0] = False
            dialog.destroy()
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ícone
        icon_label = ctk.CTkLabel(main_frame, text="❓", font=ctk.CTkFont(size=36))
        icon_label.pack(pady=(10, 10))
        
        # Mensagem
        msg_label = ctk.CTkLabel(
            main_frame,
            text=message,
            font=ctk.CTkFont(size=13),
            wraplength=400,
            justify="center"
        )
        msg_label.pack(pady=10)
        
        # Frame dos botões
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(pady=15)
        
        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="❌ Cancelar",
            command=on_cancel,
            width=120,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        cancel_btn.pack(side="left", padx=10)
        
        confirm_btn = ctk.CTkButton(
            btn_frame,
            text="✅ Confirmar",
            command=on_confirm,
            width=120,
            fg_color="#28a745",
            hover_color="#1e7e34"
        )
        confirm_btn.pack(side="left", padx=10)
        
        # Aguardar fechamento do diálogo
        dialog.wait_window()
        
        return result[0]
