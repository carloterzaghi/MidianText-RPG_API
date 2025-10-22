import customtkinter as ctk
import api_client
from tkinter import messagebox

class MissionMapWindow(ctk.CTkToplevel):
    """Janela do mapa da missão"""
    def __init__(self, parent, controller, character, mission_id, mission_data):
        super().__init__(parent)
        
        self.controller = controller
        self.character = character
        self.mission_id = mission_id
        self.current_room_data = mission_data['current_room']
        self.character_status = mission_data['character_status']
        
        self.title(f"Missão: {mission_data['mission_info']['name']}")
        self.geometry("1200x800")
        
        # Tornar modal
        self.transient(parent)
        self.grab_set()
        
        # Centralizar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.winfo_screenheight() // 2) - (800 // 2)
        self.geometry(f"1200x800+{x}+{y}")
        
        self.create_ui()
        self.display_room()
    
    def create_ui(self):
        """Cria a interface do mapa"""
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header com status do personagem
        header_frame = ctk.CTkFrame(main_frame, height=80, fg_color=("#d0d0d0", "#1a1a1a"))
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        header_frame.grid_propagate(False)
        
        hp = self.character_status.get('hp', 100)
        hp_max = self.character_status.get('hp_max', 100)
        gold = self.character_status.get('gold', 0)
        
        self.status_label = ctk.CTkLabel(
            header_frame,
            text=f"❤️ HP: {hp}/{hp_max}  |  💰 Ouro: {gold}  |  👤 {self.character['name']}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.status_label.pack(pady=20)
        
        # Área central com scroll
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # ScrollableFrame para o conteúdo
        self.scroll_frame = ctk.CTkScrollableFrame(content_frame, fg_color="transparent")
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")
        
        # Frame para mapa visual
        self.map_frame = ctk.CTkFrame(self.scroll_frame, fg_color=("#e8e8e8", "#2a2a2a"))
        self.map_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para descrição da sala
        self.description_frame = ctk.CTkFrame(self.scroll_frame, fg_color=("#f5f5f5", "#1e1e1e"))
        self.description_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para ações
        self.actions_frame = ctk.CTkFrame(self.scroll_frame, fg_color=("#e0e0e0", "#252525"))
        self.actions_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Frame para log de mensagens
        self.log_frame = ctk.CTkFrame(self.scroll_frame, fg_color=("#ececec", "#1a1a1a"))
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        log_title = ctk.CTkLabel(self.log_frame, text="📜 Log de Eventos", font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(pady=10)
        
        self.log_text = ctk.CTkTextbox(self.log_frame, height=100, fg_color=("#ffffff", "#0d0d0d"))
        self.log_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Botão fechar
        close_button = ctk.CTkButton(
            main_frame,
            text="← Sair da Missão",
            command=self.destroy,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            height=40
        )
        close_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(5, 10))
    
    def display_room(self):
        """Exibe a sala atual"""
        # Limpar frames
        for widget in self.map_frame.winfo_children():
            widget.destroy()
        for widget in self.description_frame.winfo_children():
            widget.destroy()
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        room = self.current_room_data
        
        # ========== MAPA VISUAL ==========
        map_title = ctk.CTkLabel(
            self.map_frame,
            text=f"🗺️ {room['name']}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        map_title.pack(pady=15)
        
        # Criar representação visual simples do mapa
        visual_map = ctk.CTkFrame(self.map_frame, fg_color=("#d0d0d0", "#1a1a1a"))
        visual_map.pack(pady=10, padx=20)
        
        # Grade 3x3 para o mapa
        for i in range(3):
            visual_map.grid_rowconfigure(i, weight=1)
            visual_map.grid_columnconfigure(i, weight=1)
        
        # Sala atual no centro
        center_label = ctk.CTkLabel(
            visual_map,
            text="📍\nVOCÊ\nESTÁ\nAQUI",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#4caf50", "#2e7d32"),
            corner_radius=10,
            width=100,
            height=100
        )
        center_label.grid(row=1, column=1, padx=5, pady=5)
        
        # Mostrar saídas disponíveis
        exits = room.get('exits', {})
        exit_positions = {
            'esquerda': (1, 0),
            'direita': (1, 2),
            'frente': (0, 1),
            'tras': (2, 1),
            'voltar': (2, 1),
            'saida': (0, 1)
        }
        
        for direction, next_room in exits.items():
            pos = exit_positions.get(direction, (1, 1))
            emoji = "🚪" if next_room != "fim" else "🏆"
            text = direction.capitalize() if next_room != "fim" else "SAÍDA"
            
            exit_label = ctk.CTkLabel(
                visual_map,
                text=f"{emoji}\n{text}",
                font=ctk.CTkFont(size=12),
                fg_color=("#2196f3", "#1565c0"),
                corner_radius=8,
                width=90,
                height=90
            )
            exit_label.grid(row=pos[0], column=pos[1], padx=5, pady=5)
        
        # ========== DESCRIÇÃO ==========
        desc_title = ctk.CTkLabel(
            self.description_frame,
            text="📖 Descrição",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        desc_title.pack(pady=10)
        
        desc_text = ctk.CTkTextbox(
            self.description_frame,
            height=120,
            fg_color=("#ffffff", "#0d0d0d"),
            wrap="word"
        )
        desc_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        desc_text.insert("1.0", room['description'])
        desc_text.configure(state="disabled")
        
        # ========== AÇÕES ==========
        actions_title = ctk.CTkLabel(
            self.actions_frame,
            text="⚔️ Ações Disponíveis",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        actions_title.pack(pady=10)
        
        # Grid de ações
        actions_grid = ctk.CTkFrame(self.actions_frame, fg_color="transparent")
        actions_grid.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        col = 0
        row = 0
        
        # Botões de movimento
        if exits:
            move_label = ctk.CTkLabel(actions_grid, text="🚶 Mover-se:", font=ctk.CTkFont(size=14, weight="bold"))
            move_label.grid(row=row, column=0, columnspan=3, pady=(5, 10), sticky="w")
            row += 1
            
            for direction in exits.keys():
                btn = ctk.CTkButton(
                    actions_grid,
                    text=f"→ {direction.capitalize()}",
                    command=lambda d=direction: self.move(d),
                    fg_color="#2196f3",
                    hover_color="#1565c0",
                    width=150
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
        
        # Inimigos
        enemies = room.get('enemies', [])
        if enemies:
            row += 1
            col = 0
            enemy_label = ctk.CTkLabel(actions_grid, text="⚔️ Inimigos:", font=ctk.CTkFont(size=14, weight="bold"))
            enemy_label.grid(row=row, column=0, columnspan=3, pady=(10, 10), sticky="w")
            row += 1
            
            for enemy in enemies:
                btn = ctk.CTkButton(
                    actions_grid,
                    text=f"⚔️ Lutar: {enemy['name']} (HP: {enemy['hp']})",
                    command=lambda e=enemy: self.fight(e['id']),
                    fg_color="#f44336",
                    hover_color="#c62828",
                    width=250
                )
                btn.grid(row=row, column=col, padx=5, pady=5, columnspan=2)
                col += 2
                if col >= 3:
                    col = 0
                    row += 1
        
        # Tesouros
        treasures = room.get('treasures', [])
        if treasures:
            row += 1
            col = 0
            treasure_label = ctk.CTkLabel(actions_grid, text="💎 Tesouros:", font=ctk.CTkFont(size=14, weight="bold"))
            treasure_label.grid(row=row, column=0, columnspan=3, pady=(10, 10), sticky="w")
            row += 1
            
            for treasure in treasures:
                btn = ctk.CTkButton(
                    actions_grid,
                    text=f"💰 Coletar: {treasure['name']}",
                    command=lambda t=treasure: self.collect(t['id']),
                    fg_color="#ff9800",
                    hover_color="#f57c00",
                    width=200
                )
                btn.grid(row=row, column=col, padx=5, pady=5)
                col += 1
                if col >= 3:
                    col = 0
                    row += 1
    
    def add_log(self, message):
        """Adiciona mensagem ao log"""
        self.log_text.configure(state="normal")
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
    
    def update_status(self, character_status):
        """Atualiza o status do personagem"""
        self.character_status = character_status
        hp = character_status.get('hp', 100)
        hp_max = character_status.get('hp_max', 100)
        gold = character_status.get('gold', 0)
        
        self.status_label.configure(
            text=f"❤️ HP: {hp}/{hp_max}  |  💰 Ouro: {gold}  |  👤 {self.character['name']}"
        )
    
    def move(self, direction):
        """Move o personagem para outra sala"""
        token = self.controller.access_token
        result = api_client.mission_action(
            token,
            self.character['name'],
            self.mission_id,
            "move",
            direction
        )
        
        if 'error' in result:
            messagebox.showerror("Erro", f"Erro ao mover: {result['error']}")
            return
        
        if result.get('success'):
            self.add_log(result.get('message', 'Você se moveu.'))
            
            # Verificar se completou a missão
            if result.get('mission_progress', {}).get('completed'):
                rewards = result['mission_progress']['rewards']
                messagebox.showinfo(
                    "Missão Completada! 🎉",
                    f"Parabéns! Você completou a missão!\n\n"
                    f"Recompensas:\n"
                    f"💰 Ouro: {rewards.get('gold', 0)}\n"
                    f"⭐ Experiência: {rewards.get('exp', 0)}"
                )
                self.destroy()
                return
            
            # Atualizar sala atual
            self.current_room_data = result.get('current_room', {})
            self.update_status(result.get('character_status', {}))
            self.display_room()
    
    def fight(self, enemy_id):
        """Luta contra um inimigo"""
        token = self.controller.access_token
        result = api_client.mission_action(
            token,
            self.character['name'],
            self.mission_id,
            "fight",
            enemy_id
        )
        
        if 'error' in result:
            messagebox.showerror("Erro", f"Erro ao lutar: {result['error']}")
            return
        
        if result.get('success'):
            self.add_log(result.get('message', 'Você atacou!'))
            self.current_room_data = result.get('current_room', {})
            self.update_status(result.get('character_status', {}))
            self.display_room()
            
            # Verificar se o personagem morreu
            if self.character_status.get('hp', 0) <= 0:
                messagebox.showwarning("Game Over", "Você foi derrotado! A missão falhou.")
                self.destroy()
    
    def collect(self, treasure_id):
        """Coleta um tesouro"""
        token = self.controller.access_token
        result = api_client.mission_action(
            token,
            self.character['name'],
            self.mission_id,
            "collect",
            treasure_id
        )
        
        if 'error' in result:
            messagebox.showerror("Erro", f"Erro ao coletar: {result['error']}")
            return
        
        if result.get('success'):
            self.add_log(result.get('message', 'Você coletou um tesouro!'))
            self.current_room_data = result.get('current_room', {})
            self.update_status(result.get('character_status', {}))
            self.display_room()


class MissionsWindow(ctk.CTkToplevel):
    """Janela de seleção de missões"""
    def __init__(self, parent, controller, character):
        super().__init__(parent)
        
        self.controller = controller
        self.character = character
        
        self.title("Missões Disponíveis")
        self.geometry("800x600")
        
        # Tornar modal
        self.transient(parent)
        self.grab_set()
        
        # Centralizar
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"800x600+{x}+{y}")
        
        self.create_ui()
        self.load_missions()
    
    def create_ui(self):
        """Cria a interface"""
        # Frame principal
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="🗺️ Missões Disponíveis",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Informações do personagem
        char_info = ctk.CTkLabel(
            main_frame,
            text=f"👤 Personagem: {self.character['name']} | Nível: {self.character.get('level', 1)}",
            font=ctk.CTkFont(size=16)
        )
        char_info.pack(pady=(0, 20))
        
        # Frame scrollable para missões
        self.missions_frame = ctk.CTkScrollableFrame(main_frame, fg_color="transparent")
        self.missions_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Botão fechar
        close_button = ctk.CTkButton(
            main_frame,
            text="← Voltar",
            command=self.destroy,
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=40
        )
        close_button.pack(fill="x")
    
    def load_missions(self):
        """Carrega as missões disponíveis"""
        token = self.controller.access_token
        result = api_client.get_missions(token)
        
        if 'error' in result:
            # Verificar se é erro de autenticação
            if '401' in str(result.get('error', '')):
                error_label = ctk.CTkLabel(
                    self.missions_frame,
                    text="⚠️ Sessão expirada! Faça login novamente.",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    text_color="#f44336"
                )
                error_label.pack(pady=20)
                
                logout_btn = ctk.CTkButton(
                    self.missions_frame,
                    text="← Voltar para Login",
                    command=lambda: (self.destroy(), self.controller.show_screen("LoginScreen")),
                    fg_color="#2196f3",
                    hover_color="#1565c0"
                )
                logout_btn.pack(pady=10)
            else:
                error_label = ctk.CTkLabel(
                    self.missions_frame,
                    text=f"❌ Erro ao carregar missões: {result['error']}",
                    font=ctk.CTkFont(size=14)
                )
                error_label.pack(pady=20)
            return
        
        missions = result.get('missions', [])
        
        if not missions:
            no_missions_label = ctk.CTkLabel(
                self.missions_frame,
                text="Nenhuma missão disponível no momento.",
                font=ctk.CTkFont(size=14)
            )
            no_missions_label.pack(pady=20)
            return
        
        # Exibir cada missão
        for mission in missions:
            self.create_mission_card(mission)
    
    def create_mission_card(self, mission):
        """Cria um card para uma missão"""
        card = ctk.CTkFrame(
            self.missions_frame,
            fg_color=("#f0f0f0", "#2e2e2e"),
            corner_radius=10
        )
        card.pack(fill="x", padx=10, pady=10)
        
        # Título da missão
        title = ctk.CTkLabel(
            card,
            text=f"🗡️ {mission['name']}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(anchor="w", padx=20, pady=(15, 5))
        
        # Descrição
        desc = ctk.CTkLabel(
            card,
            text=mission['description'],
            font=ctk.CTkFont(size=13),
            wraplength=700,
            justify="left"
        )
        desc.pack(anchor="w", padx=20, pady=5)
        
        # Informações
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(fill="x", padx=20, pady=10)
        
        difficulty_colors = {
            "Fácil": "#4caf50",
            "Médio": "#ff9800",
            "Difícil": "#f44336"
        }
        
        difficulty_color = difficulty_colors.get(mission['difficulty'], "#9e9e9e")
        
        difficulty = ctk.CTkLabel(
            info_frame,
            text=f"⚔️ Dificuldade: {mission['difficulty']}",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=difficulty_color
        )
        difficulty.pack(side="left", padx=(0, 20))
        
        min_level = ctk.CTkLabel(
            info_frame,
            text=f"📊 Nível mínimo: {mission['min_level']}",
            font=ctk.CTkFont(size=12)
        )
        min_level.pack(side="left", padx=(0, 20))
        
        rewards = mission.get('rewards', {})
        gold_reward = ctk.CTkLabel(
            info_frame,
            text=f"💰 Recompensa: {rewards.get('gold', 0)} ouro",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#ffc107"
        )
        gold_reward.pack(side="left")
        
        # Botão iniciar
        char_level = self.character.get('level', 1)
        can_start = char_level >= mission['min_level']
        
        start_button = ctk.CTkButton(
            card,
            text="🚀 Iniciar Missão" if can_start else f"🔒 Requer Nível {mission['min_level']}",
            command=lambda m=mission: self.start_mission(m),
            fg_color="#28a745" if can_start else "#6c757d",
            hover_color="#218838" if can_start else "#5a6268",
            state="normal" if can_start else "disabled",
            height=40
        )
        start_button.pack(fill="x", padx=20, pady=(10, 15))
    
    def start_mission(self, mission):
        """Inicia uma missão"""
        token = self.controller.access_token
        result = api_client.start_mission(
            token,
            self.character['name'],
            mission['id']
        )
        
        if 'error' in result:
            messagebox.showerror("Erro", f"Erro ao iniciar missão: {result['error']}")
            return
        
        if result.get('success'):
            # Fechar janela de seleção e abrir o mapa
            self.destroy()
            MissionMapWindow(self.master, self.controller, self.character, mission['id'], result)
