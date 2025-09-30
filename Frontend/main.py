import customtkinter as ctk
import api_client

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MidianText RPG")
        self.state('zoomed')

        # store user data
        self.access_token = None
        self.current_user = None

        # create a container for screens
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.screens = {}

        for F in (LoginScreen, RegisterScreen, HomeScreen):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.screens[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_screen("LoginScreen")

    def show_screen(self, page_name):
        '''Show a screen for the given page name'''
        screen = self.screens[page_name]
        if page_name == "HomeScreen":
            screen.on_enter()
        screen.tkraise()

class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame principal para centralizar o conteúdo
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0)

        label = ctk.CTkLabel(main_frame, text="Login", font=ctk.CTkFont(size=32, weight="bold"))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=(40, 30))

        self.username_input = ctk.CTkEntry(main_frame, placeholder_text="Username", width=300, height=40)
        self.username_input.grid(row=1, column=0, columnspan=2, padx=40, pady=10)

        self.password_input = ctk.CTkEntry(main_frame, placeholder_text="Password", show="*", width=300, height=40)
        self.password_input.grid(row=2, column=0, columnspan=2, padx=40, pady=10)

        self.show_password = False
        self.toggle_password_btn = ctk.CTkButton(
            main_frame, text="Mostrar", width=80, height=40, command=self.toggle_password
        )
        self.toggle_password_btn.grid(row=2, column=1, padx=(0, 40), sticky="e")

        login_button = ctk.CTkButton(main_frame, text="Login", command=self.do_login, width=300, height=40)
        login_button.grid(row=3, column=0, columnspan=2, padx=40, pady=20)

        self.error_label = ctk.CTkLabel(main_frame, text="", text_color="red")
        self.error_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        register_button = ctk.CTkButton(
            main_frame,
            text="Não tem uma conta? Registre-se",
            command=lambda: controller.show_screen("RegisterScreen"),
            fg_color="transparent",
            text_color="#2e86de",
            hover_color="#1e1e1e"
        )
        register_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 20))

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_input.configure(show="")
            self.toggle_password_btn.configure(text="Ocultar")
        else:
            self.password_input.configure(show="*")
            self.toggle_password_btn.configure(text="Mostrar")

    def do_login(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if not username or not password:
            self.error_label.configure(text='Usuário e senha são obrigatórios.')
            return

        response = api_client.login_user(username, password)

        # Ajuste para aceitar tanto "key" quanto "access_token"
        token = response.get('key') or response.get('access_token') if response else None
        
        if response and token:
            self.controller.access_token = token
            self.controller.current_user = username
            self.controller.show_screen('HomeScreen')
            self.username_input.delete(0, 'end')
            self.password_input.delete(0, 'end')
            self.error_label.configure(text="")
        else:
            # Mensagem de sucesso do registro
            if response.get("success_message"):
                self.error_label.configure(text=response["success_message"], text_color="green")
            else:
                error_msg = response.get('detail') or 'Login falhou. Verifique suas credenciais.'
                if isinstance(error_msg, list):
                    error_msg = error_msg[0].get('msg', 'Erro desconhecido')
                self.error_label.configure(text=str(error_msg), text_color="red")


class RegisterScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Frame principal para centralizar o conteúdo
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0)

        label = ctk.CTkLabel(main_frame, text="Registrar", font=ctk.CTkFont(size=32, weight="bold"))
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=(40, 30))

        self.username_input = ctk.CTkEntry(main_frame, placeholder_text="Username", width=300, height=40)
        self.username_input.grid(row=1, column=0, columnspan=2, padx=40, pady=10)

        self.password_input = ctk.CTkEntry(main_frame, placeholder_text="Password", show="*", width=300, height=40)
        self.password_input.grid(row=2, column=0, columnspan=2, padx=40, pady=10)

        self.show_password = False
        self.toggle_password_btn = ctk.CTkButton(
            main_frame, text="Mostrar", width=80, height=40, command=self.toggle_password
        )
        self.toggle_password_btn.grid(row=2, column=1, padx=(0, 40), sticky="e")

        register_button = ctk.CTkButton(main_frame, text="Registrar", command=self.do_register, width=300, height=40)
        register_button.grid(row=3, column=0, columnspan=2, padx=40, pady=20)

        self.status_label = ctk.CTkLabel(main_frame, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        back_button = ctk.CTkButton(
            main_frame,
            text="Já tem uma conta? Faça o login",
            command=lambda: controller.show_screen("LoginScreen"),
            fg_color="transparent",
            text_color="#2e86de",
            hover_color="#1e1e1e"
        )
        back_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 20))

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_input.configure(show="")
            self.toggle_password_btn.configure(text="Ocultar")
        else:
            self.password_input.configure(show="*")
            self.toggle_password_btn.configure(text="Mostrar")

    def do_register(self):
        username = self.username_input.get()
        password = self.password_input.get()

        if not username or not password:
            self.status_label.configure(text='Usuário e senha são obrigatórios.', text_color="red")
            return

        # Mostrar que está processando
        self.status_label.configure(text='Registrando usuário...', text_color="blue")
        self.update()  # Atualizar interface

        response = api_client.register_user(username, password)

        # Ajuste para esperar por "message" igual ao teste_front.py
        if response and response.get('message') == 'User created successfully':
            # Mostrar sucesso do registro
            self.status_label.configure(text='✅ Usuário criado! Fazendo login automático...', text_color="green")
            self.update()  # Atualizar interface
            
            # Fazer login automático
            login_response = api_client.login_user(username, password)
            
            if login_response and 'access_token' in login_response:
                # Login automático bem-sucedido
                self.controller.access_token = login_response['access_token']
                self.controller.current_user = username
                
                # Limpar campos
                self.username_input.delete(0, 'end')
                self.password_input.delete(0, 'end')
                self.status_label.configure(text="")
                
                # Redirecionar para HomeScreen
                self.controller.show_screen('HomeScreen')
            elif login_response and 'key' in login_response:
                # Login automático bem-sucedido (formato alternativo)
                self.controller.access_token = login_response['key']
                self.controller.current_user = username
                
                # Limpar campos
                self.username_input.delete(0, 'end')
                self.password_input.delete(0, 'end')
                self.status_label.configure(text="")
                
                # Redirecionar para HomeScreen
                self.controller.show_screen('HomeScreen')
            else:
                # Registro OK, mas login automático falhou
                self.controller.screens["LoginScreen"].error_label.configure(
                    text="Usuário criado com sucesso! Faça o login.", text_color="green"
                )
                self.controller.show_screen("LoginScreen")
                self.username_input.delete(0, 'end')
                self.password_input.delete(0, 'end')
                self.status_label.configure(text="")
        else:
            error_msg = response.get('detail') or response.get('message') or 'Falha no registro.'
            if isinstance(error_msg, list):
                error_msg = error_msg[0].get('msg', 'Erro desconhecido')
            self.status_label.configure(text=str(error_msg), text_color="red")


class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Top bar
        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        self.user_label = ctk.CTkLabel(top_frame, text="Usuário: ", font=ctk.CTkFont(size=16))
        self.user_label.grid(row=0, column=0, sticky="w")

        logout_button = ctk.CTkButton(top_frame, text="Sair", width=80, height=30, command=self.logout)
        logout_button.grid(row=0, column=1, sticky="e")

        # Main title
        self.title_label = ctk.CTkLabel(self, text="Seus Personagens", font=ctk.CTkFont(size=32, weight="bold"))
        self.title_label.grid(row=1, column=0, padx=20, pady=20)

        # Botão para criar personagem
        self.create_button = ctk.CTkButton(self, text="⚔️ Criar Novo Personagem", command=self.check_and_create_character)
        self.create_button.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="e")

        # Personagens list
        self.personagens_list = ctk.CTkScrollableFrame(self, label_text="Personagens")
        self.personagens_list.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")


    def on_enter(self):
        self.user_label.configure(text=f"Usuário: {self.controller.current_user}")
        self.load_personagens()

    def load_personagens(self):
        token = self.controller.access_token
        if not token:
            self.controller.show_screen('LoginScreen')
            return

        # Clear old widgets
        for widget in self.personagens_list.winfo_children():
            widget.destroy()

        response = api_client.get_personagens(token)
        
        # Tratar resposta da nova API
        if isinstance(response, list):
            personagens = response
        elif response and 'personagens' in response:
            personagens = response['personagens']
        else:
            personagens = []

        # Atualizar título com contador
        personagens_count = len(personagens) if personagens else 0
        self.title_label.configure(text=f"Seus Personagens ({personagens_count}/3)")
        
        # Atualizar estado do botão
        if personagens_count >= 3:
            self.create_button.configure(text="⚠️ Limite Atingido (3/3)", state="disabled")
        else:
            self.create_button.configure(text="⚔️ Criar Novo Personagem", state="normal")

        if personagens and len(personagens) > 0:
            for i, personagem in enumerate(personagens):
                nome = personagem.get('name', personagem.get('nome', 'Nome não encontrado'))
                classe = personagem.get('character_class', personagem.get('classe', 'Classe não encontrada'))
                
                # Frame for each character
                char_frame = ctk.CTkFrame(self.personagens_list, fg_color=("#f0f0f0", "#2e2e2e"), corner_radius=10)
                char_frame.pack(fill="x", padx=10, pady=5)

                # Nome do personagem à esquerda
                info_text = f"{nome} - {classe}"
                name_label = ctk.CTkLabel(char_frame, text=info_text, font=ctk.CTkFont(size=16), anchor="w")
                name_label.pack(side="left", padx=15, pady=10, expand=True, fill="x")

                # Frame para botões à direita
                buttons_frame = ctk.CTkFrame(char_frame, fg_color="transparent")
                buttons_frame.pack(side="right", padx=15, pady=10)

                # Botão deletar
                def make_delete_cmd(char):
                    return lambda: self.confirm_delete_character(char)
                
                delete_btn = ctk.CTkButton(
                    buttons_frame,
                    text="🗑️ Deletar",
                    width=90,
                    height=30,
                    fg_color="#d32f2f",
                    hover_color="#b71c1c",
                    command=make_delete_cmd(personagem)
                )
                delete_btn.pack(side="right", padx=(5, 0))

                # Botão detalhes
                def make_details_cmd(char):
                    return lambda: self.show_character_details(char)
                
                details_btn = ctk.CTkButton(
                    buttons_frame,
                    text="🧾 Detalhes", 
                    width=90,
                    height=30,
                    command=make_details_cmd(personagem)
                )
                details_btn.pack(side="right", padx=(0, 5))
        else:
            # Nenhum personagem encontrado
            no_chars_frame = ctk.CTkFrame(self.personagens_list, fg_color=("#f9f9f9", "#1e1e1e"), corner_radius=10)
            no_chars_frame.pack(fill="x", padx=10, pady=20)
            
            welcome_label = ctk.CTkLabel(no_chars_frame, text="🎮 Bem-vindo ao Midian Text RPG!", 
                                       font=ctk.CTkFont(size=18, weight="bold"))
            welcome_label.pack(pady=(20, 10))
            
            info_label = ctk.CTkLabel(no_chars_frame, text="Você ainda não tem personagens.\nClique em 'Criar Novo Personagem' para começar sua aventura!\n\n📝 Limite: Você pode criar até 3 personagens.")
            info_label.pack(pady=(0, 20))
            
            # Se há erro na resposta
            if response and isinstance(response, dict) and 'error' in response:
                error_label = ctk.CTkLabel(self.personagens_list, text=f"Erro: {response['error']}", text_color="red")
                error_label.pack(padx=10, pady=5)
    
    def check_and_create_character(self):
        """Verifica o limite de personagens antes de abrir o diálogo de criação."""
        token = self.controller.access_token
        if not token:
            self.controller.show_screen('LoginScreen')
            return
        
        # Buscar personagens atuais
        response = api_client.get_personagens(token)
        
        if response and not isinstance(response, dict):
            # Resposta válida com lista de personagens
            personagens_count = len(response)
            
            if personagens_count >= 3:
                # Mostrar aviso de limite atingido
                self.show_limit_reached_dialog()
                return
            
            # Se ainda pode criar, mostrar o diálogo
            self.show_create_character_dialog()
        else:
            # Se não conseguiu buscar ou lista vazia, permitir criação
            self.show_create_character_dialog()
    
    def show_limit_reached_dialog(self):
        """Mostra diálogo informando que o limite foi atingido."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Limite Atingido")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ícone e título
        title_label = ctk.CTkLabel(main_frame, text="⚠️ Limite Atingido", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Mensagem
        message_label = ctk.CTkLabel(main_frame, 
                                   text="Você já criou 3 personagens,\no limite máximo permitido.\n\nPara criar um novo personagem,\nvocê deve deletar um existente.",
                                   font=ctk.CTkFont(size=14),
                                   justify="center")
        message_label.pack(pady=20)
        
        # Informação adicional
        info_label = ctk.CTkLabel(main_frame, 
                                text="💡 Dica: Clique no botão 'Deletar' ao lado\ndo personagem que deseja remover.",
                                font=ctk.CTkFont(size=12),
                                text_color="gray",
                                justify="center")
        info_label.pack(pady=10)
        
        # Botão OK
        ok_button = ctk.CTkButton(main_frame, text="✅ Entendi", command=dialog.destroy,
                                 font=ctk.CTkFont(size=14))
        ok_button.pack(pady=20)

    def show_create_character_dialog(self):
        """Mostra diálogo para criar personagem."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Criar Novo Personagem")
        dialog.geometry("600x700")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (700 // 2)
        dialog.geometry(f"600x700+{x}+{y}")
        
        # Scroll frame para todo o conteúdo
        scroll_frame = ctk.CTkScrollableFrame(dialog)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        title_label = ctk.CTkLabel(scroll_frame, text="Criar Personagem", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Nome do personagem
        name_label = ctk.CTkLabel(scroll_frame, text="Nome do Personagem:", font=ctk.CTkFont(size=14, weight="bold"))
        name_label.pack(pady=(10, 5))
        
        name_entry = ctk.CTkEntry(scroll_frame, placeholder_text="Digite o nome (2-20 caracteres)", width=400)
        name_entry.pack(pady=5)
        
        # Classe do personagem
        class_label = ctk.CTkLabel(scroll_frame, text="Classe:", font=ctk.CTkFont(size=14, weight="bold"))
        class_label.pack(pady=(15, 5))
        
        class_var = ctk.StringVar(value="Assassino")
        class_menu = ctk.CTkOptionMenu(scroll_frame, values=["Assassino", "Arqueiro", "Mago", "Soldado"], 
                                      variable=class_var, width=400)
        class_menu.pack(pady=5)
        
        # Cor do personagem
        color_label = ctk.CTkLabel(scroll_frame, text="Cor:", font=ctk.CTkFont(size=14, weight="bold"))
        color_label.pack(pady=(15, 5))
        
        color_var = ctk.StringVar(value="🔴 Vermelho")
        color_menu = ctk.CTkOptionMenu(scroll_frame, values=["🔴 Vermelho", "🟢 Verde", "🔵 Azul", "⚫ Cinza"], 
                                      variable=color_var, width=400)
        color_menu.pack(pady=5)
        
        # Informações da cor
        color_info_label = ctk.CTkLabel(scroll_frame, text="🔴 Vermelho > 🟢 Verde > 🔵 Azul > 🔴 Vermelho | ⚫ Cinza = Neutro\nVantagem = x1.5 dano",
                                      font=ctk.CTkFont(size=12), text_color="gray")
        color_info_label.pack(pady=5)
        
        # Frame para estatísticas
        stats_frame = ctk.CTkFrame(scroll_frame)
        stats_frame.pack(fill="x", pady=20)
        
        stats_title = ctk.CTkLabel(stats_frame, text="📊 Estatísticas da Classe", font=ctk.CTkFont(size=16, weight="bold"))
        stats_title.pack(pady=10)
        
        # Container para as estatísticas (será atualizado dinamicamente)
        stats_container = ctk.CTkFrame(stats_frame)
        stats_container.pack(fill="x", padx=10, pady=10)
        
        # Função para carregar e exibir estatísticas
        def update_stats(selected_class=None):
            # Limpar container
            for widget in stats_container.winfo_children():
                widget.destroy()
            
            # Buscar informações das classes
            try:
                classes_data = api_client.get_available_classes()
                if not classes_data or "error" in classes_data:
                    stats_label = ctk.CTkLabel(stats_container, text="Erro ao carregar estatísticas", text_color="red")
                    stats_label.pack()
                    return
                
                current_class = selected_class or class_var.get()
                if current_class in classes_data:
                    stats = classes_data[current_class]['stats']
                    
                    # Criar grid de estatísticas
                    stats_info = [
                        ("❤️ HP Máximo:", stats['hp_max']),
                        ("💪 Força:", stats['strg']),
                        ("✨ Magia:", stats['mag']),
                        ("⚡ Velocidade:", stats['spd']),
                        ("🍀 Sorte:", stats['luck']),
                        ("🛡️ Defesa:", stats['defe']),
                        ("🚀 Movimento:", stats['mov'])
                    ]
                    
                    for i, (label, value) in enumerate(stats_info):
                        row = i // 2
                        col = i % 2
                        
                        stat_frame = ctk.CTkFrame(stats_container)
                        stat_frame.grid(row=row, column=col, padx=5, pady=2, sticky="ew")
                        
                        stat_text = f"{label} {value}"
                        stat_label = ctk.CTkLabel(stat_frame, text=stat_text, font=ctk.CTkFont(size=12))
                        stat_label.pack(pady=5)
                    
                    # Configurar colunas para expansão
                    stats_container.grid_columnconfigure(0, weight=1)
                    stats_container.grid_columnconfigure(1, weight=1)
                    
                    # Mostrar habilidades se disponíveis
                    if 'habilidades' in classes_data[current_class]:
                        hab_label = ctk.CTkLabel(stats_container, text="🎯 Habilidades:", font=ctk.CTkFont(size=12, weight="bold"))
                        hab_label.grid(row=len(stats_info)//2 + 1, column=0, columnspan=2, pady=(10, 5))
                        
                        for j, habilidade in enumerate(classes_data[current_class]['habilidades']):
                            hab_text = ctk.CTkLabel(stats_container, text=f"• {habilidade}", font=ctk.CTkFont(size=10), 
                                                  text_color="gray", wraplength=500)
                            hab_text.grid(row=len(stats_info)//2 + 2 + j, column=0, columnspan=2, sticky="w", padx=10)
                            
            except Exception as e:
                error_label = ctk.CTkLabel(stats_container, text=f"Erro: {str(e)}", text_color="red")
                error_label.pack()
        
        # Atualizar estatísticas quando a classe mudar
        class_menu.configure(command=update_stats)
        
        # Carregar estatísticas iniciais
        update_stats()
        
        # Status label
        status_label = ctk.CTkLabel(scroll_frame, text="", font=ctk.CTkFont(size=12))
        status_label.pack(pady=10)
        
        # Botões
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def create_character():
            name = name_entry.get().strip()
            character_class = class_var.get()
            color_display = color_var.get()
            
            # Extrair cor real do display
            color_map = {
                "🔴 Vermelho": "vermelho",
                "🟢 Verde": "verde", 
                "🔵 Azul": "azul",
                "⚫ Cinza": "cinza"
            }
            color = color_map.get(color_display, "cinza")
            
            if not name:
                status_label.configure(text="Por favor, digite um nome para o personagem.", text_color="red")
                return
                
            if len(name) < 2 or len(name) > 20:
                status_label.configure(text="O nome deve ter entre 2 e 20 caracteres.", text_color="red")
                return
            
            status_label.configure(text="Criando personagem...", text_color="blue")
            dialog.update()
            
            # Criar personagem usando a API com cor
            result = api_client.create_character(self.controller.access_token, name, character_class, color)
            
            if result and not result.get('error'):
                status_label.configure(text="✅ Personagem criado com sucesso!", text_color="green")
                dialog.update()
                dialog.after(1500, dialog.destroy)
                # Recarregar lista de personagens
                self.load_personagens()
            else:
                error_msg = result.get('error', 'Erro desconhecido') if result else 'Erro na comunicação'
                status_label.configure(text=f"Erro: {error_msg}", text_color="red")
        
        create_btn = ctk.CTkButton(button_frame, text="🎯 Criar Personagem", command=create_character, 
                                  font=ctk.CTkFont(size=14, weight="bold"))
        create_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="❌ Cancelar", command=dialog.destroy)
        cancel_btn.pack(side="left", padx=10)
        
        name_entry.focus()
    
    def show_character_details(self, character):
        """Mostra detalhes completos do personagem."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Detalhes - {character.get('name', 'Personagem')}")
        dialog.geometry("650x800")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (650 // 2)
        y = (dialog.winfo_screenheight() // 2) - (800 // 2)
        dialog.geometry(f"650x800+{x}+{y}")
        
        # Scroll frame para os detalhes
        scroll_frame = ctk.CTkScrollableFrame(dialog)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título com nome e classe
        name = character.get('name', 'Nome não encontrado')
        char_class = character.get('character_class', 'Classe não encontrada')
        title_label = ctk.CTkLabel(scroll_frame, text=f"⚔️ {name}", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=(0, 5))
        
        class_label = ctk.CTkLabel(scroll_frame, text=f"🎭 {char_class}", 
                                  font=ctk.CTkFont(size=16), text_color="gray")
        class_label.pack(pady=(0, 20))
        
        # Informações básicas
        basic_frame = ctk.CTkFrame(scroll_frame)
        basic_frame.pack(fill="x", pady=10)
        
        basic_title = ctk.CTkLabel(basic_frame, text="📋 Informações Básicas", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        basic_title.pack(pady=10)
        
        # Extrair cor e emoji
        color = character.get('color', 'cinza')
        color_emojis = {
            'vermelho': '🔴',
            'verde': '🟢', 
            'azul': '🔵',
            'cinza': '⚫'
        }
        color_emoji = color_emojis.get(color, '⚫')
        
        basic_details = [
            ("🆔 ID", character.get('id', 'N/A')[:12] + '...' if character.get('id') else 'N/A'),
            ("🎚️ Nível", character.get('level', 1)),
            ("🎨 Cor", f"{color_emoji} {color.title()}"),
        ]
        
        for label, value in basic_details:
            detail_frame = ctk.CTkFrame(basic_frame, fg_color="transparent")
            detail_frame.pack(fill="x", pady=2)
            
            label_widget = ctk.CTkLabel(detail_frame, text=f"{label}:", width=120, anchor="w")
            label_widget.pack(side="left", padx=(10, 5))
            
            value_widget = ctk.CTkLabel(detail_frame, text=str(value), anchor="w")
            value_widget.pack(side="left")
        
        # Estatísticas
        stats_frame = ctk.CTkFrame(scroll_frame)
        stats_frame.pack(fill="x", pady=10)
        
        stats_title = ctk.CTkLabel(stats_frame, text="📊 Estatísticas", 
                                  font=ctk.CTkFont(size=16, weight="bold"))
        stats_title.pack(pady=10)
        
        # Verificar se existem status detalhados
        status_data = character.get('status', {})
        if status_data:
            # Usar dados do status (nova estrutura)
            stats_details = [
                ("❤️ HP Máximo", status_data.get('hp_max', 0)),
                ("💗 HP Atual", status_data.get('hp_atual', status_data.get('hp_max', 0))),
                ("💪 Força", status_data.get('strg', 0)),
                ("✨ Magia", status_data.get('mag', 0)),
                ("⚡ Velocidade", status_data.get('spd', 0)),
                ("🍀 Sorte", status_data.get('luck', 0)),
                ("🛡️ Defesa", status_data.get('defe', 0)),
                ("🚀 Movimento", status_data.get('mov', 0)),
            ]
        else:
            # Usar dados antigos (compatibilidade)
            stats_details = [
                ("❤️ HP Máximo", character.get('hp_max', 0)),
                ("💗 HP Atual", character.get('hp_tmp', character.get('hp_max', 0))),
                ("💪 Força", character.get('strg', 0)),
                ("✨ Magia", character.get('mag', 0)),
                ("⚡ Velocidade", character.get('spd', 0)),
                ("🍀 Sorte", character.get('luck', 0)),
                ("🛡️ Defesa", character.get('defe', 0)),
                ("🚀 Movimento", character.get('mov', 0)),
            ]
        
        # Criar grid 2x4 para estatísticas
        stats_container = ctk.CTkFrame(stats_frame)
        stats_container.pack(fill="x", padx=10, pady=10)
        
        for i, (label, value) in enumerate(stats_details):
            row = i // 2
            col = i % 2
            
            stat_frame = ctk.CTkFrame(stats_container)
            stat_frame.grid(row=row, column=col, padx=5, pady=3, sticky="ew")
            
            stat_text = f"{label}: {value}"
            stat_label = ctk.CTkLabel(stat_frame, text=stat_text, font=ctk.CTkFont(size=12))
            stat_label.pack(pady=5)
        
        # Configurar colunas para expansão
        stats_container.grid_columnconfigure(0, weight=1)
        stats_container.grid_columnconfigure(1, weight=1)
        
        # Habilidades
        habilidades = character.get('habilidades', [])
        if habilidades:
            hab_frame = ctk.CTkFrame(scroll_frame)
            hab_frame.pack(fill="x", pady=10)
            
            hab_title = ctk.CTkLabel(hab_frame, text="🎯 Habilidades", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
            hab_title.pack(pady=10)
            
            for habilidade in habilidades:
                hab_item = ctk.CTkLabel(hab_frame, text=f"• {habilidade}", 
                                       font=ctk.CTkFont(size=12), anchor="w", 
                                       wraplength=580, justify="left")
                hab_item.pack(fill="x", padx=15, pady=2, anchor="w")
        
        # Itens
        itens = character.get('itens', {})
        if itens:
            itens_frame = ctk.CTkFrame(scroll_frame)
            itens_frame.pack(fill="x", pady=10)
            
            itens_title = ctk.CTkLabel(itens_frame, text="🎒 Inventário", 
                                      font=ctk.CTkFont(size=16, weight="bold"))
            itens_title.pack(pady=10)
            
            # Mapear emojis para tipos de itens conhecidos
            item_emojis = {
                'Poção de Cura': '🧪',
                'Fuga': '📜',
                'Adagas Gêmeas': '🗡️',
                'Arco Élfico': '🏹',
                'Cajado Arcano': '🔮',
                'Escudo de Ferro': '🛡️'
            }
            
            for item_name, quantity in itens.items():
                emoji = item_emojis.get(item_name, '📦')
                item_text = f"{emoji} {item_name}: {quantity}x"
                
                item_label = ctk.CTkLabel(itens_frame, text=item_text, 
                                         font=ctk.CTkFont(size=12), anchor="w")
                item_label.pack(fill="x", padx=15, pady=2, anchor="w")
        
        # Informações adicionais
        if character.get('created_at'):
            created_at = character.get('created_at', '')
            # Tentar formatar a data se possível
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
                formatted_date = dt.strftime('%d/%m/%Y às %H:%M')
                
                date_frame = ctk.CTkFrame(scroll_frame)
                date_frame.pack(fill="x", pady=10)
                
                date_label = ctk.CTkLabel(date_frame, text=f"📅 Criado em: {formatted_date}", 
                                         font=ctk.CTkFont(size=10), text_color="gray")
                date_label.pack(pady=5)
            except:
                pass  # Se não conseguir formatar, não mostra
        
        # Botão fechar
        close_btn = ctk.CTkButton(scroll_frame, text="❌ Fechar", command=dialog.destroy,
                                 font=ctk.CTkFont(size=14))
        close_btn.pack(pady=20)

    def confirm_delete_character(self, character):
        """Mostra diálogo de confirmação para deletar personagem."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar Exclusão")
        dialog.geometry("600x500")
        dialog.transient(self)
        dialog.grab_set()
        dialog.resizable(False, False)
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"600x500+{x}+{y}")

        # Frame principal com scroll se necessário
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Ícone de aviso
        warning_label = ctk.CTkLabel(main_frame, text="⚠️", 
                                    font=ctk.CTkFont(size=48))
        warning_label.pack(pady=(30, 15))
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="Confirmar Exclusão", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(0, 15))
        
        # Nome do personagem
        character_name = character.get('name', 'Personagem')
        character_class = character.get('character_class', 'Classe')
        
        char_info_label = ctk.CTkLabel(main_frame, 
                                      text=f"'{character_name}' - {character_class}",
                                      font=ctk.CTkFont(size=18, weight="bold"),
                                      text_color="#d32f2f")
        char_info_label.pack(pady=(0, 20))
        
        # Mensagem de confirmação
        message_label = ctk.CTkLabel(main_frame, 
                                   text="Tem certeza que deseja deletar\neste personagem?\n\n⚠️ Esta ação não pode ser desfeita!",
                                   font=ctk.CTkFont(size=16),
                                   justify="center")
        message_label.pack(pady=(10, 30))
        
        def delete_character():
            """Executa a exclusão do personagem."""
            token = self.controller.access_token
            if not token:
                dialog.destroy()
                self.controller.show_screen('LoginScreen')
                return
            
            result = api_client.delete_character(token, character_name)
            
            if result and not result.get('error'):
                dialog.destroy()
                # Recarregar lista de personagens
                self.load_personagens()
                # Mostrar mensagem de sucesso
                self.show_success_message(f"Personagem '{character_name}' deletado com sucesso!")
            else:
                error_msg = result.get('error', 'Erro desconhecido') if result else 'Erro na comunicação'
                dialog.destroy()
                self.show_error_message(f"Erro ao deletar personagem: {error_msg}")
        
        # Frame dos botões - versão ultra-simplificada
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(pady=30, padx=30, fill="x")
        
        # Container interno para os botões
        inner_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
        inner_frame.pack(pady=20, expand=True)
        
        # Botão Cancelar
        cancel_btn = ctk.CTkButton(inner_frame, 
                                  text="❌ Cancelar", 
                                  command=dialog.destroy,
                                  width=150,
                                  height=50,
                                  font=ctk.CTkFont(size=16, weight="bold"))
        cancel_btn.pack(side="left", padx=20)
        
        # Botão Deletar
        delete_btn = ctk.CTkButton(inner_frame, 
                                  text="🗑️ Deletar", 
                                  command=delete_character,
                                  width=150,
                                  height=50,
                                  fg_color="#d32f2f",
                                  hover_color="#b71c1c",
                                  font=ctk.CTkFont(size=16, weight="bold"))
        delete_btn.pack(side="left", padx=20)

    def show_success_message(self, message):
        """Mostra uma mensagem de sucesso."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Sucesso")
        dialog.geometry("450x300")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"450x300+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ícone de sucesso
        success_label = ctk.CTkLabel(main_frame, text="✅", 
                                    font=ctk.CTkFont(size=36))
        success_label.pack(pady=(20, 10))
        
        # Mensagem
        message_label = ctk.CTkLabel(main_frame, text=message,
                                   font=ctk.CTkFont(size=14),
                                   justify="center")
        message_label.pack(pady=10)
        
        # Botão OK
        ok_btn = ctk.CTkButton(main_frame, text="✅ OK", command=dialog.destroy,
                              font=ctk.CTkFont(size=14))
        ok_btn.pack(pady=15)
        
        # Auto fechar após 3 segundos
        dialog.after(3000, dialog.destroy)

    def show_error_message(self, message):
        """Mostra uma mensagem de erro."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Erro")
        dialog.geometry("350x200")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"350x200+{x}+{y}")
        
        # Frame principal
        main_frame = ctk.CTkFrame(dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ícone de erro
        error_label = ctk.CTkLabel(main_frame, text="❌", 
                                  font=ctk.CTkFont(size=36))
        error_label.pack(pady=(20, 10))
        
        # Mensagem
        message_label = ctk.CTkLabel(main_frame, text=message,
                                   font=ctk.CTkFont(size=14),
                                   justify="center",
                                   text_color="#d32f2f")
        message_label.pack(pady=10)
        
        # Botão OK
        ok_btn = ctk.CTkButton(main_frame, text="❌ OK", command=dialog.destroy,
                              font=ctk.CTkFont(size=14))
        ok_btn.pack(pady=15)

    def logout(self):
        self.controller.access_token = None
        self.controller.current_user = None
        self.controller.show_screen('LoginScreen')
        # Clear the list
        for widget in self.personagens_list.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
