import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from api_client import login_user, register_user, get_personagens, create_character, get_available_classes
import json

class CharacterCreatorApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Midian Text RPG - Criador de Personagens")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Token do usuário logado
        self.token = None
        self.username = None
        
        # Dados das classes
        self.classes_data = {}
        
        # Configurar estilo
        self.setup_styles()
        
        # Criar interface
        self.create_login_interface()
        
    def setup_styles(self):
        """Configura os estilos da aplicação."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores personalizadas
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Subtitle.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Info.TLabel', font=('Arial', 10), foreground='#7f8c8d')
        style.configure('Stats.TLabel', font=('Arial', 9), foreground='#2c3e50')
        style.configure('Success.TLabel', font=('Arial', 10), foreground='#27ae60')
        style.configure('Error.TLabel', font=('Arial', 10), foreground='#e74c3c')
        
    def create_login_interface(self):
        """Cria a interface de login."""
        # Limpar a janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Título
        title_label = ttk.Label(main_frame, text="Midian Text RPG", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Frame de login
        login_frame = ttk.LabelFrame(main_frame, text="Login", padding="20")
        login_frame.pack(expand=True)
        
        # Campos de login
        ttk.Label(login_frame, text="Usuário:").grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = ttk.Entry(login_frame, width=30)
        self.username_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(login_frame, text="Senha:").grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = ttk.Entry(login_frame, show="*", width=30)
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Botões
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.login_button = ttk.Button(button_frame, text="Login", command=self.login)
        self.login_button.pack(side='left', padx=5)
        
        self.register_button = ttk.Button(button_frame, text="Registrar", command=self.register)
        self.register_button.pack(side='left', padx=5)
        
        # Label para mensagens
        self.login_message_label = ttk.Label(login_frame, text="", style='Info.TLabel')
        self.login_message_label.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Bind Enter key para login
        self.root.bind('<Return>', lambda event: self.login())
        
    def login(self):
        """Faz login do usuário."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_login_message("Por favor, preencha todos os campos.", "error")
            return
            
        self.disable_login_buttons()
        self.show_login_message("Fazendo login...", "info")
        self.root.update()
        
        result = login_user(username, password)
        
        if "error" in result:
            self.show_login_message(f"Erro no login: {result['error']}", "error")
            self.enable_login_buttons()
        elif "access_token" in result:
            self.token = result["access_token"]
            self.username = username
            self.show_login_message("Login realizado com sucesso!", "success")
            # Limpar campos
            self.clear_login_fields()
            self.force_redirect_to_main()
        else:
            self.show_login_message("Erro no login: Resposta inválida do servidor.", "error")
            self.enable_login_buttons()
    
    def register(self):
        """Registra um novo usuário."""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            self.show_login_message("Por favor, preencha todos os campos.", "error")
            return
            
        if len(password) < 6:
            self.show_login_message("A senha deve ter pelo menos 6 caracteres.", "error")
            return
        
        self.disable_login_buttons()
        self.show_login_message("Registrando usuário...", "info")
        self.root.update()
        
        result = register_user(username, password)
        
        print(f"🔍 Resultado do registro: {result}")
        
        if "error" in result:
            self.show_login_message(f"Erro no registro: {result['error']}", "error")
            self.enable_login_buttons()
        else:
            self.show_login_message("Usuário registrado! Fazendo login automático...", "success")
            self.root.update()
            
            print(f"Fazendo login automático para: {username}")
            
            # Fazer login automaticamente após registro bem-sucedido
            login_result = login_user(username, password)
            
            print(f"Resultado do login automático: {login_result}")
            
            if "error" in login_result:
                self.show_login_message(f"Registro realizado, mas erro no login automático: {login_result['error']}", "error")
                self.enable_login_buttons()
            elif "access_token" in login_result:
                self.token = login_result["access_token"]
                self.username = username
                self.show_login_message("🎉 Bem-vindo! Redirecionando...", "success")
                print(f"Token obtido: {self.token[:20]}...")
                print("Iniciando redirecionamento...")
                # Limpar campos
                self.clear_login_fields()
                # Redirecionamento imediato forçado
                self.root.update()
                self.force_redirect_to_main()
            else:
                self.show_login_message("Registro realizado, mas falha no login automático. Tente fazer login manualmente.", "error")
                self.enable_login_buttons()
    
    def show_login_message(self, message, msg_type):
        """Mostra uma mensagem na tela de login."""
        if msg_type == "error":
            style = 'Error.TLabel'
        elif msg_type == "success":
            style = 'Success.TLabel'
        else:
            style = 'Info.TLabel'
            
        self.login_message_label.configure(text=message, style=style)
    
    def clear_login_fields(self):
        """Limpa os campos de login."""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def disable_login_buttons(self):
        """Desabilita os botões de login durante operações."""
        if hasattr(self, 'login_button') and hasattr(self, 'register_button'):
            self.login_button.configure(state='disabled')
            self.register_button.configure(state='disabled')
    
    def enable_login_buttons(self):
        """Habilita os botões de login após operações."""
        if hasattr(self, 'login_button') and hasattr(self, 'register_button'):
            self.login_button.configure(state='normal')
            self.register_button.configure(state='normal')
    
    def force_redirect_to_main(self):
        """Força redirecionamento para a interface principal."""
        print("Executando redirecionamento forçado...")
        try:
            # Pequeno delay para garantir que a mensagem seja vista
            self.root.after(800, self.create_main_interface)
        except Exception as e:
            print(f"Erro no redirecionamento: {e}")
            # Fallback direto
            self.create_main_interface()
    
    def create_main_interface(self):
        """Cria a interface principal com criação e listagem de personagens."""
        print(f"Criando interface principal para usuário: {self.username}")
        print(f"Token disponível: {'Sim' if self.token else 'Não'}")
        
        # Limpar a janela
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Cabeçalho
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text=f"Bem-vindo, {self.username}!", style='Title.TLabel').pack(side='left')
        ttk.Button(header_frame, text="Logout", command=self.logout).pack(side='right')
        
        # Notebook para abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(expand=True, fill='both')
        
        # Aba de criação de personagem
        self.create_character_tab()
        
        # Aba de listagem de personagens
        self.create_characters_list_tab()
        
        # Carregar dados das classes
        self.load_classes_data()
        
        # Verificar se o usuário tem personagens e redirecionar se necessário (com delay)
        self.root.after(1000, self.check_and_redirect_for_character_creation)
        
    def create_character_tab(self):
        """Cria a aba de criação de personagens."""
        # Frame da aba
        create_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(create_frame, text="Criar Personagem")
        
        # Título
        ttk.Label(create_frame, text="Criar Novo Personagem", style='Subtitle.TLabel').pack(pady=(0, 20))
        
        # Frame do formulário
        form_frame = ttk.Frame(create_frame)
        form_frame.pack(fill='x')
        
        # Nome do personagem
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill='x', pady=10)
        
        ttk.Label(name_frame, text="Nome do Personagem:").pack(side='left')
        self.character_name_entry = ttk.Entry(name_frame, width=30)
        self.character_name_entry.pack(side='left', padx=(10, 0))
        self.character_name_entry.bind('<KeyRelease>', lambda e: self.update_button_states())
        
        # Seleção de classe
        class_frame = ttk.Frame(form_frame)
        class_frame.pack(fill='x', pady=10)
        
        ttk.Label(class_frame, text="Classe:").pack(side='left')
        self.character_class_var = tk.StringVar()
        self.character_class_combo = ttk.Combobox(class_frame, textvariable=self.character_class_var,
                                                  state='readonly', width=27)
        self.character_class_combo.pack(side='left', padx=(10, 0))
        self.character_class_combo.bind('<<ComboboxSelected>>', self.on_class_selected)
        
        # Seleção de cor
        color_frame = ttk.Frame(form_frame)
        color_frame.pack(fill='x', pady=10)
        
        ttk.Label(color_frame, text="Cor:").pack(side='left')
        self.character_color_var = tk.StringVar(value="cinza")
        self.character_color_combo = ttk.Combobox(color_frame, textvariable=self.character_color_var,
                                                 state='readonly', width=27)
        self.character_color_combo.pack(side='left', padx=(10, 0))
        self.character_color_combo.bind('<<ComboboxSelected>>', self.on_color_selected)
        
        # Frame para mostrar estatísticas da classe
        self.stats_frame = ttk.LabelFrame(form_frame, text="📊 Estatísticas da Classe", padding="15")
        self.stats_frame.pack(fill='x', pady=20)
        
        # Descrição da classe
        self.class_description_frame = ttk.LabelFrame(form_frame, text="📖 Descrição da Classe", padding="15")
        self.class_description_frame.pack(fill='x', pady=(0, 20))
        
        self.class_description_label = ttk.Label(self.class_description_frame, text="Selecione uma classe para ver a descrição", 
                                                style='Info.TLabel', wraplength=600)
        self.class_description_label.pack()
        
        # Informações sobre cores e vantagens
        self.color_info_frame = ttk.LabelFrame(form_frame, text="🎨 Sistema de Cores", padding="15")
        self.color_info_frame.pack(fill='x', pady=(0, 20))
        
        self.color_info_label = ttk.Label(self.color_info_frame,
                                         text="🔴 Vermelho > 🟢 Verde > 🔵 Azul > 🔴 Vermelho | ⚫ Cinza = Neutro\nVantagem = x1.5 dano",
                                         style='Info.TLabel', wraplength=600, justify='center')
        self.color_info_label.pack()
        
        # Frame para botões
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=20)
        
        # Botão para criar (preview)
        self.create_button = ttk.Button(button_frame, text="🎯 Criar Personagem", command=self.create_character)
        self.create_button.pack(side='left', padx=5)
        
        # Botão para salvar (confirmar)
        self.save_button = ttk.Button(button_frame, text="💾 Salvar Personagem", command=self.save_character, state='disabled')
        self.save_button.pack(side='left', padx=5)
        
        # Botão limpar
        self.clear_button = ttk.Button(button_frame, text="🗑️ Limpar", command=self.clear_form)
        self.clear_button.pack(side='left', padx=5)
        
        # Label para mensagens
        self.create_message_label = ttk.Label(form_frame, text="", style='Info.TLabel')
        self.create_message_label.pack(pady=10)
        
    def create_characters_list_tab(self):
        """Cria a aba de listagem de personagens."""
        # Frame da aba
        list_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(list_frame, text="Meus Personagens")
        
        # Título e botões
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(header_frame, text="Meus Personagens", style='Subtitle.TLabel').pack(side='left')
        
        # Frame para os botões
        buttons_frame = ttk.Frame(header_frame)
        buttons_frame.pack(side='right')
        
        ttk.Button(buttons_frame, text="➕ Criar Novo", command=self.go_to_create_tab).pack(side='left', padx=5)
        ttk.Button(buttons_frame, text="🔄 Atualizar", command=self.load_characters).pack(side='left')
        
        # Frame para lista de personagens
        self.characters_frame = ttk.Frame(list_frame)
        self.characters_frame.pack(expand=True, fill='both')
        
        # Scrollbar para a lista
        canvas = tk.Canvas(self.characters_frame)
        scrollbar = ttk.Scrollbar(self.characters_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def load_classes_data(self):
        """Carrega os dados das classes disponíveis."""
        result = get_available_classes()
        
        if "error" in result:
            self.show_create_message(f"Erro ao carregar classes: {result['error']}", "error")
        else:
            self.classes_data = result
            class_names = list(self.classes_data.keys())
            self.character_class_combo['values'] = class_names
        
        # Carregar cores disponíveis
        self.load_colors_data()
    
    def load_colors_data(self):
        """Carrega os dados das cores disponíveis."""
        from api_client import get_available_colors
        result = get_available_colors()
        
        if "error" in result:
            self.show_create_message(f"Erro ao carregar cores: {result['error']}", "error")
        else:
            self.colors_data = result
            # Criar lista de cores com emojis
            color_options = []
            for color_key, color_info in result.get('cores', {}).items():
                color_options.append(f"{color_info['emoji']} {color_key.title()}")
            
            if hasattr(self, 'character_color_combo'):
                self.character_color_combo['values'] = color_options
                self.character_color_combo.set("⚫ Cinza")  # Padrão
    
    def check_and_redirect_for_character_creation(self):
        """Verifica se o usuário tem personagens e redireciona para criação se não tiver."""
        print(f"Verificando personagens para o usuário: {self.username}")
        
        # Buscar personagens do usuário
        result = get_personagens(self.token)
        
        print(f"Resultado da busca: {result}")
        
        if "error" not in result and isinstance(result, list):
            print(f"Número de personagens encontrados: {len(result)}")
            
            if len(result) == 0:  # Usuário não tem personagens
                print("Redirecionando para aba de criação de personagens...")
                # Selecionar a aba de criação de personagens (índice 0)
                self.notebook.select(0)
                # Mostrar mensagem explicativa
                self.show_welcome_message()
                print("Redirecionamento concluído!")
            else:
                print("Redirecionando para aba de listagem de personagens...")
                # Usuário tem personagens, mostrar a aba de listagem (índice 1)
                self.notebook.select(1)
                # Carregar personagens na aba
                self.load_characters()
                print("Redirecionamento para listagem concluído!")
        else:
            print("Erro ao buscar personagens ou resultado inválido")
            print(f"Detalhes: {result}")
            # Em caso de erro, mostrar aba de criação por padrão
            self.notebook.select(0)
            self.show_welcome_message()
    
    def show_welcome_message(self):
        """Mostra mensagem de boas-vindas para usuários sem personagens."""
        def show_message():
            welcome_text = f"Bem-vindo ao Midian Text RPG, {self.username}!\n\nVocê ainda não tem personagens. Vamos criar seu primeiro aventureiro!\nEscolha uma classe abaixo e comece sua jornada épica! ⚔️"
            self.show_create_message(welcome_text, "info")
            # Dar foco no campo de nome para facilitar a digitação
            if hasattr(self, 'character_name_entry'):
                self.character_name_entry.focus_set()
        
        # Aguardar 500ms para garantir que a interface esteja carregada
        self.root.after(500, show_message)
            
    def on_class_selected(self, event=None):
        """Atualiza as estatísticas quando uma classe é selecionada."""
        selected_class = self.character_class_var.get()
        
        # Limpar frame de estatísticas
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Limpar descrição
        self.class_description_label.configure(text="Selecione uma classe para ver a descrição")
            
        if selected_class and selected_class in self.classes_data:
            stats = self.classes_data[selected_class]['stats']
            
            # Descrições das classes
            class_descriptions = {
                "Assassino": "🗡️ Especialista em velocidade e ataques furtivos. Alta velocidade e sorte, mas baixa defesa. Ideal para ataques rápidos e precisos.",
                "Arqueiro": "🏹 Combatente balanceado com foco em ataques à distância. Boa velocidade e força, perfeito para táticas versáteis.",
                "Mago": "🧙 Mestre das artes arcanas com grande poder mágico. Alta magia mas baixa defesa física. Devastador com feitiços.",
                "Soldado": "🛡️ Tanque resistente com alta defesa e força. Baixa velocidade mas capaz de absorver muito dano. Protetor da equipe."
            }
            
            # Atualizar descrição
            description = class_descriptions.get(selected_class, "Descrição não disponível")
            self.class_description_label.configure(text=description)
            
            # Título dos stats
            title_label = ttk.Label(self.stats_frame, text=f"⚔️ {selected_class}", style='Subtitle.TLabel')
            title_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))
            
            # Criar grid de estatísticas com cores
            stats_info = [
                ("❤️ HP Máximo:", stats['hp_max'], "#e74c3c"),
                ("💪 Força:", stats['strg'], "#e67e22"),
                ("✨ Magia:", stats['mag'], "#9b59b6"),
                ("⚡ Velocidade:", stats['spd'], "#3498db"),
                ("🍀 Sorte:", stats['luck'], "#f1c40f"),
                ("🛡️ Defesa:", stats['defe'], "#2ecc71"),
                ("🚀 Movimento:", stats['mov'], "#34495e")
            ]
            
            for i, (label, value, color) in enumerate(stats_info):
                row = (i // 2) + 1  # +1 por causa do título
                col = (i % 2) * 2
                
                # Label do stat
                stat_label = ttk.Label(self.stats_frame, text=label, style='Stats.TLabel')
                stat_label.grid(row=row, column=col, sticky='w', padx=5, pady=3)
                
                # Valor do stat com barra de progresso visual
                value_frame = ttk.Frame(self.stats_frame)
                value_frame.grid(row=row, column=col+1, sticky='w', padx=10, pady=3)
                
                # Número
                value_label = ttk.Label(value_frame, text=f"{value:2d}", style='Stats.TLabel', width=3)
                value_label.pack(side='left')
                
                # Barra visual (usando caracteres)
                max_stat = 20  # Valor máximo possível
                bar_length = 10
                filled = int((value / max_stat) * bar_length)
                bar = "█" * filled + "░" * (bar_length - filled)
                bar_label = ttk.Label(value_frame, text=bar, font=('Courier', 8))
                bar_label.pack(side='left', padx=(5, 0))
            
            # Habilitar botão de criar se nome também estiver preenchido
            self.update_button_states()
    
    def update_button_states(self):
        """Atualiza o estado dos botões baseado no preenchimento do formulário."""
        name = self.character_name_entry.get().strip()
        class_selected = self.character_class_var.get()
        color_selected = self.character_color_var.get()
        
        if name and class_selected and color_selected:
            self.create_button.configure(state='normal')
        else:
            self.create_button.configure(state='disabled')
            self.save_button.configure(state='disabled')
    
    def on_color_selected(self, event=None):
        """Atualiza as informações quando uma cor é selecionada."""
        selected_color_display = self.character_color_var.get()
        
        if not selected_color_display or not hasattr(self, 'colors_data'):
            return
            
        # Extrair a cor real do display (ex: "🔴 Vermelho" -> "vermelho")
        color_name = selected_color_display.split(' ', 1)[1].lower() if ' ' in selected_color_display else "cinza"
        
        cores_info = self.colors_data.get('cores', {})
        if color_name in cores_info:
            color_info = cores_info[color_name]
            
            # Atualizar informação da cor
            info_text = f"{color_info['name']}: {color_info['description']}\n"
            info_text += f"Bônus: {color_info['damage_bonus']}"
            
            self.color_info_label.configure(text=info_text)
        
        # Atualizar estado dos botões
        self.update_button_states()
    
    def create_character(self):
        """Cria um novo personagem."""
        name = self.character_name_entry.get().strip()
        character_class = self.character_class_var.get()
        color_display = self.character_color_var.get()
        
        if not name:
            self.show_create_message("Por favor, digite um nome para o personagem.", "error")
            return
            
        if not character_class:
            self.show_create_message("Por favor, selecione uma classe.", "error")
            return
            
        if not color_display:
            self.show_create_message("Por favor, selecione uma cor.", "error")
            return
            
        # Extrair cor real do display
        color = color_display.split(' ', 1)[1].lower() if ' ' in color_display else "cinza"
            
        # Validação do nome
        if len(name) < 2 or len(name) > 20:
            self.show_create_message("O nome deve ter entre 2 e 20 caracteres.", "error")
            return
            
        self.show_create_message("Criando personagem...", "info")
        self.root.update()
        
        result = create_character(self.token, name, character_class, color)
        
        if "error" in result:
            self.show_create_message(f"Erro ao criar personagem: {result['error']}", "error")
        else:
            self.show_create_message(f"Personagem '{name}' ({color}) criado com sucesso! 🎉", "success")
            
            # Habilitar botão de salvar (mesmo que já tenha salvado, para consistência da UI)
            if hasattr(self, 'save_button'):
                self.save_button.configure(state='normal')
            
            # Atualizar lista de personagens
            self.load_characters()
            
            # Auto-redirect para aba de personagens após 3 segundos
            self.root.after(3000, lambda: self.notebook.select(1))
    
    def show_create_message(self, message, msg_type):
        """Mostra uma mensagem na aba de criação."""
        if msg_type == "error":
            style = 'Error.TLabel'
        elif msg_type == "success":
            style = 'Success.TLabel'
        else:
            style = 'Info.TLabel'
        
        # Verificar se o label existe antes de tentar configurá-lo
        if hasattr(self, 'create_message_label'):
            self.create_message_label.configure(text=message, style=style)
    
    def load_characters(self):
        """Carrega e exibe a lista de personagens do usuário."""
        result = get_personagens(self.token)
        
        # Limpar frame de personagens
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if "error" in result:
            ttk.Label(self.scrollable_frame, text=f"Erro ao carregar personagens: {result['error']}",
                     style='Error.TLabel').pack(pady=20)
        elif not result:
            # Frame para mensagem de personagens vazios
            empty_frame = ttk.Frame(self.scrollable_frame)
            empty_frame.pack(expand=True, pady=50)
            
            ttk.Label(empty_frame, text="Nenhum personagem encontrado!", 
                     style='Subtitle.TLabel').pack(pady=10)
            ttk.Label(empty_frame, text="Comece sua aventura criando seu primeiro personagem!", 
                     style='Info.TLabel').pack(pady=5)
            
            # Botão para ir para criação
            create_btn = ttk.Button(empty_frame, text="⚔️ Criar Meu Primeiro Personagem", 
                                   command=self.go_to_create_tab)
            create_btn.pack(pady=20)
        else:
            for i, character in enumerate(result):
                self.create_character_card(character, i)
    
    def create_character_card(self, character, index):
        """Cria um card para exibir informações do personagem."""
        # Frame do card
        card_frame = ttk.LabelFrame(self.scrollable_frame, text=f"{character.get('name', 'Sem nome')} - {character.get('character_class', 'Sem classe')}",
                                   padding="15")
        card_frame.pack(fill='x', padx=5, pady=5)
        
        # Informações básicas
        info_frame = ttk.Frame(card_frame)
        info_frame.pack(fill='x')
        
        # Coluna esquerda - Informações gerais
        left_frame = ttk.Frame(info_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        
        ttk.Label(left_frame, text=f"Nível: {character.get('level', 1)}", style='Info.TLabel').pack(anchor='w')
        ttk.Label(left_frame, text=f"ID: {character.get('id', 'N/A')[:8]}...", style='Info.TLabel').pack(anchor='w')
        
        # Coluna direita - Estatísticas
        right_frame = ttk.Frame(info_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        # Grid de estatísticas
        stats_info = [
            ("HP:", f"{character.get('hp_tmp', 0)}/{character.get('hp_max', 0)}"),
            ("Força:", character.get('strg', 0)),
            ("Magia:", character.get('mag', 0)),
            ("Velocidade:", character.get('spd', 0)),
            ("Sorte:", character.get('luck', 0)),
            ("Defesa:", character.get('defe', 0)),
            ("Movimento:", character.get('mov', 0))
        ]
        
        for i, (label, value) in enumerate(stats_info):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(right_frame, text=label, style='Stats.TLabel').grid(
                row=row, column=col, sticky='w', padx=5, pady=1
            )
            ttk.Label(right_frame, text=str(value), style='Stats.TLabel').grid(
                row=row, column=col+1, sticky='w', padx=5, pady=1
            )
    
    def go_to_create_tab(self):
        """Navega para a aba de criação de personagem."""
        self.notebook.select(0)
        # Limpar mensagem anterior e mostrar nova mensagem
        self.show_create_message("✨ Pronto para criar um novo personagem!", "info")
        # Dar foco no campo de nome
        if hasattr(self, 'character_name_entry'):
            self.character_name_entry.focus_set()
    
    def logout(self):
        """Faz logout do usuário."""
        self.token = None
        self.username = None
        self.create_login_interface()
    
    def save_character(self):
        """Salva o personagem atual (funcionalidade em desenvolvimento)."""
        name = self.character_name_entry.get().strip()
        character_class = self.character_class_var.get()
        
        if not name or not character_class:
            self.show_create_message("Complete todos os campos antes de salvar.", "error")
            return
            
        # Por enquanto, usar a mesma funcionalidade do create_character
        self.show_create_message("Salvando personagem...", "info")
        self.create_character()
    
    def clear_form(self):
        """Limpa o formulário de criação."""
        self.character_name_entry.delete(0, tk.END)
        self.character_class_var.set("")
        self.character_color_var.set("⚫ Cinza")
        
        # Limpar stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        # Limpar descrição
        if hasattr(self, 'class_description_label'):
            self.class_description_label.configure(text="Selecione uma classe para ver a descrição")
        
        # Limpar informação de cor
        if hasattr(self, 'color_info_label'):
            self.color_info_label.configure(text="🔴 Vermelho > 🟢 Verde > 🔵 Azul > 🔴 Vermelho | ⚫ Cinza = Neutro\nVantagem = x1.5 dano")
        
        # Atualizar estado dos botões
        if hasattr(self, 'update_button_states'):
            self.update_button_states()
        
        self.show_create_message("Formulário limpo.", "info")

    def run(self):
        """Inicia a aplicação."""
        self.root.mainloop()

if __name__ == "__main__":
    app = CharacterCreatorApp()
    app.run()