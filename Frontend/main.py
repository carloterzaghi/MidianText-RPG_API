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
        title_label = ctk.CTkLabel(self, text="Seus Personagens", font=ctk.CTkFont(size=32, weight="bold"))
        title_label.grid(row=1, column=0, padx=20, pady=20)

        # Botão para criar personagem
        create_button = ctk.CTkButton(self, text="⚔️ Criar Novo Personagem", command=self.show_create_character_dialog)
        create_button.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="e")

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

        if personagens and len(personagens) > 0:
            for i, personagem in enumerate(personagens):
                nome = personagem.get('name', personagem.get('nome', 'Nome não encontrado'))
                classe = personagem.get('character_class', personagem.get('classe', 'Classe não encontrada'))
                
                # Frame for each character
                char_frame = ctk.CTkFrame(self.personagens_list, fg_color=("#f0f0f0", "#2e2e2e"), corner_radius=10)
                char_frame.pack(fill="x", padx=10, pady=5)
                
                char_frame.grid_columnconfigure(0, weight=1)

                # Character name and class
                info_text = f"{nome} - {classe}"
                name_label = ctk.CTkLabel(char_frame, text=info_text, font=ctk.CTkFont(size=16))
                name_label.grid(row=0, column=0, padx=15, pady=10, sticky="w")

                # "Ver detalhes" button
                details_button = ctk.CTkButton(
                    char_frame, 
                    text="Ver detalhes", 
                    width=120,
                    command=lambda p=personagem: self.show_character_details(p)
                )
                details_button.grid(row=0, column=1, padx=15, pady=10, sticky="e")
        else:
            # Nenhum personagem encontrado
            no_chars_frame = ctk.CTkFrame(self.personagens_list, fg_color=("#f9f9f9", "#1e1e1e"), corner_radius=10)
            no_chars_frame.pack(fill="x", padx=10, pady=20)
            
            welcome_label = ctk.CTkLabel(no_chars_frame, text="🎮 Bem-vindo ao Midian Text RPG!", 
                                       font=ctk.CTkFont(size=18, weight="bold"))
            welcome_label.pack(pady=(20, 10))
            
            info_label = ctk.CTkLabel(no_chars_frame, text="Você ainda não tem personagens.\nClique em 'Criar Novo Personagem' para começar sua aventura!")
            info_label.pack(pady=(0, 20))
            
            # Se há erro na resposta
            if response and isinstance(response, dict) and 'error' in response:
                error_label = ctk.CTkLabel(self.personagens_list, text=f"Erro: {response['error']}", text_color="red")
                error_label.pack(padx=10, pady=5)
    
    def show_create_character_dialog(self):
        """Mostra diálogo para criar personagem."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Criar Novo Personagem")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Título
        title_label = ctk.CTkLabel(dialog, text="Criar Personagem", font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=20)
        
        # Nome do personagem
        name_label = ctk.CTkLabel(dialog, text="Nome do Personagem:")
        name_label.pack(pady=(10, 5))
        
        name_entry = ctk.CTkEntry(dialog, placeholder_text="Digite o nome", width=300)
        name_entry.pack(pady=5)
        
        # Classe do personagem
        class_label = ctk.CTkLabel(dialog, text="Classe:")
        class_label.pack(pady=(15, 5))
        
        class_var = ctk.StringVar(value="Assassino")
        class_menu = ctk.CTkOptionMenu(dialog, values=["Assassino", "Arqueiro", "Mago", "Soldado"], 
                                      variable=class_var, width=300)
        class_menu.pack(pady=5)
        
        # Status label
        status_label = ctk.CTkLabel(dialog, text="")
        status_label.pack(pady=10)
        
        # Botões
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=20)
        
        def create_character():
            name = name_entry.get().strip()
            character_class = class_var.get()
            
            if not name:
                status_label.configure(text="Por favor, digite um nome para o personagem.", text_color="red")
                return
            
            status_label.configure(text="Criando personagem...", text_color="blue")
            dialog.update()
            
            # Criar personagem usando a API
            result = api_client.create_character(self.controller.access_token, name, character_class)
            
            if result and not result.get('error'):
                status_label.configure(text="✅ Personagem criado com sucesso!", text_color="green")
                dialog.update()
                dialog.after(1500, dialog.destroy)
                # Recarregar lista de personagens
                self.load_personagens()
            else:
                error_msg = result.get('error', 'Erro desconhecido') if result else 'Erro na comunicação'
                status_label.configure(text=f"Erro: {error_msg}", text_color="red")
        
        create_btn = ctk.CTkButton(button_frame, text="Criar", command=create_character)
        create_btn.pack(side="left", padx=10)
        
        cancel_btn = ctk.CTkButton(button_frame, text="Cancelar", command=dialog.destroy)
        cancel_btn.pack(side="left", padx=10)
        
        name_entry.focus()
    
    def show_character_details(self, character):
        """Mostra detalhes do personagem."""
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Detalhes - {character.get('name', 'Personagem')}")
        dialog.geometry("450x500")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centralizar o diálogo
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (500 // 2)
        dialog.geometry(f"450x500+{x}+{y}")
        
        # Scroll frame para os detalhes
        scroll_frame = ctk.CTkScrollableFrame(dialog)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        name = character.get('name', 'Nome não encontrado')
        char_class = character.get('character_class', 'Classe não encontrada')
        title_label = ctk.CTkLabel(scroll_frame, text=f"{name} - {char_class}", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(0, 20))
        
        # Informações do personagem
        info_frame = ctk.CTkFrame(scroll_frame)
        info_frame.pack(fill="x", pady=10)
        
        details = [
            ("ID", character.get('id', 'N/A')[:8] + '...' if character.get('id') else 'N/A'),
            ("Nível", character.get('level', 1)),
            ("HP", f"{character.get('hp_tmp', 0)}/{character.get('hp_max', 0)}"),
            ("Força", character.get('strg', 0)),
            ("Magia", character.get('mag', 0)),
            ("Velocidade", character.get('spd', 0)),
            ("Sorte", character.get('luck', 0)),
            ("Defesa", character.get('defe', 0)),
            ("Movimento", character.get('mov', 0)),
        ]
        
        for i, (label, value) in enumerate(details):
            detail_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            detail_frame.pack(fill="x", pady=2)
            
            label_widget = ctk.CTkLabel(detail_frame, text=f"{label}:", width=100, anchor="w")
            label_widget.pack(side="left", padx=(10, 5))
            
            value_widget = ctk.CTkLabel(detail_frame, text=str(value), anchor="w")
            value_widget.pack(side="left")
        
        # Botão fechar
        close_btn = ctk.CTkButton(scroll_frame, text="Fechar", command=dialog.destroy)
        close_btn.pack(pady=20)

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
