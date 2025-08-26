import tkinter as tk

class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title("Software de Login")
        self.geometry("400x300")

        # O container que irá empilhar os frames um sobre o outro
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.current_user = None
        self.frames = {}

        # Adicionar as páginas/frames
        for F in (LoginPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        # Chamar set_user se a página for a HomePage
        if cont == HomePage:
            frame.set_user(self.current_user)
        frame.tkraise()

    def logout(self):
        self.current_user = None
        self.show_frame(LoginPage)

    def attempt_login(self, username, password):
        # Credenciais fixas para este exemplo
        if username == "admin" and password == "password":
            self.current_user = username
            self.show_frame(HomePage)
            # Limpa a mensagem de erro ao fazer login com sucesso
            self.frames[LoginPage].show_error("")
        else:
            # Atualiza a mensagem de erro na LoginPage
            self.frames[LoginPage].show_error("Credenciais inválidas.")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Tela de Login")
        label.pack(pady=10, padx=10)

        # Campo Usuário
        tk.Label(self, text="Usuário:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        # Campo Senha
        tk.Label(self, text="Senha:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        # Botão de Login
        login_button = tk.Button(self, text="Login",
                            command=lambda: controller.attempt_login(
                                self.username_entry.get(),
                                self.password_entry.get()
                            ))
        login_button.pack(pady=10)

        # Rótulo de erro
        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

    def show_error(self, message):
        self.error_label.config(text=message)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        # Frame principal para o conteúdo
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        label = tk.Label(main_frame, text="Página Inicial")
        label.pack(pady=10, padx=10)

        # Rodapé
        footer_frame = tk.Frame(self, height=30)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_frame.pack_propagate(False) # Impede que os widgets filhos alterem o tamanho do frame

        self.user_label = tk.Label(footer_frame, text="")
        self.user_label.pack(side=tk.LEFT, padx=10)

        logout_button = tk.Button(footer_frame, text="Deslogar",
                                 command=lambda: controller.logout())
        logout_button.pack(side=tk.RIGHT, padx=10)

    def set_user(self, username):
        self.user_label.config(text=f"Usuário: {username}")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
