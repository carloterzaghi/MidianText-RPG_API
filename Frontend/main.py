import customtkinter as ctk
import api_client

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("MidianText RPG")
        self.geometry("400x500")

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

        self.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(self, text="Login", font=ctk.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, padx=10, pady=(40, 20))

        self.username_input = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_input.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

        # Campo de senha e botão de mostrar/ocultar
        self.password_input = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_input.grid(row=2, column=0, padx=40, pady=10, sticky="ew")

        self.show_password = False
        self.toggle_password_btn = ctk.CTkButton(
            self, text="Mostrar", width=60, command=self.toggle_password
        )
        self.toggle_password_btn.grid(row=2, column=1, padx=(0, 20), pady=10)

        login_button = ctk.CTkButton(self, text="Login", command=self.do_login)
        login_button.grid(row=3, column=0, padx=40, pady=20, sticky="ew", columnspan=2)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.grid(row=4, column=0, padx=10, pady=5, columnspan=2)

        register_button = ctk.CTkButton(
            self,
            text="Não tem uma conta? Registre-se",
            command=lambda: controller.show_screen("RegisterScreen"),
            fg_color="#2e86de",  # azul
            text_color="white",
            hover_color="#145a96"
        )
        register_button.grid(row=5, column=0, padx=10, pady=(10, 20), columnspan=2)

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

        # Ajuste para esperar por "key" igual ao teste_front.py
        if response and 'key' in response:
            self.controller.access_token = response['key']
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

        self.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(self, text="Registrar", font=ctk.CTkFont(size=20, weight="bold"))
        label.grid(row=0, column=0, padx=10, pady=(40, 20))

        self.username_input = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_input.grid(row=1, column=0, padx=40, pady=10, sticky="ew")

        # Campo de senha e botão de mostrar/ocultar
        self.password_input = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_input.grid(row=2, column=0, padx=40, pady=10, sticky="ew")

        self.show_password = False
        self.toggle_password_btn = ctk.CTkButton(
            self, text="Mostrar", width=60, command=self.toggle_password
        )
        self.toggle_password_btn.grid(row=2, column=1, padx=(0, 20), pady=10)

        register_button = ctk.CTkButton(self, text="Registrar", command=self.do_register)
        register_button.grid(row=3, column=0, padx=40, pady=20, sticky="ew", columnspan=2)

        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=4, column=0, padx=10, pady=5, columnspan=2)

        back_button = ctk.CTkButton(
            self,
            text="Já tem uma conta? Faça o login",
            command=lambda: controller.show_screen("LoginScreen"),
            fg_color="#2e86de",  # azul
            text_color="white",
            hover_color="#145a96"
        )
        back_button.grid(row=5, column=0, padx=10, pady=(10, 20), columnspan=2)

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

        response = api_client.register_user(username, password)

        # Ajuste para esperar por "message" igual ao teste_front.py
        if response and response.get('message') == 'User created successfully':
            # Passa mensagem para tela de login e troca de tela
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

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        top_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        self.user_label = ctk.CTkLabel(top_frame, text="Usuário: ", font=ctk.CTkFont(size=16))
        self.user_label.grid(row=0, column=0, sticky="w")

        logout_button = ctk.CTkButton(top_frame, text="Sair", width=60, command=self.logout)
        logout_button.grid(row=0, column=1, sticky="e")

        self.personagens_list = ctk.CTkScrollableFrame(self, label_text="Personagens")
        self.personagens_list.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")


    def on_enter(self):
        self.user_label.configure(text=f"Usuário: {self.controller.current_user}")
        self.load_personagens()

    def load_personagens(self):
        token = self.controller.access_token
        if not token:
            self.controller.show_screen('login')
            return

        # Clear old widgets
        for widget in self.personagens_list.winfo_children():
            widget.destroy()

        response = api_client.get_personagens(token)

        if response and 'personagens' in response:
            for personagem in response['personagens']:
                nome = personagem.get('nome', 'Nome não encontrado')
                item = ctk.CTkLabel(self.personagens_list, text=nome)
                item.pack(padx=10, pady=5, anchor="w")
        else:
            # Corrigido para tratar lista de erros e dicionário
            if isinstance(response, list):
                # FastAPI/Pydantic error format
                error_msg = "; ".join(
                    [err.get('msg', str(err)) for err in response]
                )
            elif isinstance(response, dict):
                error_msg = response.get('detail', 'Não foi possível carregar os personagens.')
            else:
                error_msg = 'Não foi possível carregar os personagens.'
            item = ctk.CTkLabel(self.personagens_list, text=error_msg, text_color="red")
            item.pack(padx=10, pady=5, anchor="w")

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
