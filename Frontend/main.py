import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, ObjectProperty

import api_client

# Definindo as telas
class LoginScreen(Screen):
    # ObjectProperty para referenciar os widgets do arquivo .kv
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    error_label = ObjectProperty(None)

    def do_login(self, username, password):
        """
        Chamado quando o botão de login é pressionado.
        """
        if not username or not password:
            self.error_label.text = 'Usuário e senha são obrigatórios.'
            return

        response = api_client.login_user(username, password)

        if response and 'access_token' in response:
            app = App.get_running_app()
            app.access_token = response['access_token']
            app.current_user = username # Assumindo que o nome de usuário é o que usamos para logar
            self.manager.current = 'home'
            # Limpar campos e erros ao sair
            self.username_input.text = ""
            self.password_input.text = ""
            self.error_label.text = ""
        else:
            error_msg = response.get('detail') or 'Login falhou. Verifique suas credenciais.'
            if isinstance(error_msg, list): # O FastAPI pode retornar uma lista de erros
                error_msg = error_msg[0].get('msg', 'Erro desconhecido')
            self.error_label.text = str(error_msg)


class RegisterScreen(Screen):
    username_input = ObjectProperty(None)
    password_input = ObjectProperty(None)
    status_label = ObjectProperty(None)

    def do_register(self, username, password):
        """
        Chamado quando o botão de registro é pressionado.
        """
        if not username or not password:
            self.status_label.text = 'Usuário e senha são obrigatórios.'
            self.status_label.color = (1, 0.3, 0.3, 1) # Cor de erro
            return

        response = api_client.register_user(username, password)

        if response and response.get('message') == 'User created successfully':
            self.status_label.text = 'Usuário criado com sucesso! Volte e faça o login.'
            self.status_label.color = (0.3, 1, 0.3, 1) # Cor de sucesso
            self.username_input.text = ""
            self.password_input.text = ""
        else:
            error_msg = response.get('detail') or 'Falha no registro.'
            if isinstance(error_msg, list):
                error_msg = error_msg[0].get('msg', 'Erro desconhecido')
            self.status_label.text = str(error_msg)
            self.status_label.color = (1, 0.3, 0.3, 1) # Cor de erro


from kivy.uix.label import Label

class HomeScreen(Screen):
    personagens_list = ObjectProperty(None)
    user_label = ObjectProperty(None)

    def on_enter(self):
        """
        Chamado quando a tela é exibida. Carrega os dados.
        """
        app = App.get_running_app()
        self.user_label.text = f"Usuário: {app.current_user}"
        self.load_personagens()

    def load_personagens(self):
        """
        Busca os personagens da API e popula a lista.
        """
        app = App.get_running_app()
        token = app.access_token
        if not token:
            # Se não houver token, volta para o login
            self.manager.current = 'login'
            return

        # Limpa a lista antiga
        self.personagens_list.clear_widgets()

        response = api_client.get_personagens(token)

        if response and 'personagens' in response:
            for personagem in response['personagens']:
                # Assumindo que cada personagem é um dicionário com uma chave 'nome'
                nome = personagem.get('nome', 'Nome não encontrado')
                item = Label(text=nome, size_hint_y=None, height=40)
                self.personagens_list.add_widget(item)
        else:
            error_msg = response.get('detail', 'Não foi possível carregar os personagens.')
            item = Label(text=error_msg, size_hint_y=None, height=40, color=(1,0,0,1))
            self.personagens_list.add_widget(item)

    def logout(self):
        """
        Limpa o estado do usuário e volta para a tela de login.
        """
        app = App.get_running_app()
        app.access_token = None
        app.current_user = None
        self.manager.current = 'login'
        # Limpa a lista ao sair
        self.personagens_list.clear_widgets()

# O ScreenManager
class MyScreenManager(ScreenManager):
    pass

# A classe principal da App
class MainApp(App):
    # Propriedades para armazenar o estado global
    access_token = StringProperty(None)
    current_user = StringProperty(None)

    def build(self):
        # O Kivy carrega automaticamente o arquivo 'main.kv'
        # e o associa a esta classe App.
        # O widget raiz no .kv deve ser o MyScreenManager.
        return MyScreenManager()

if __name__ == '__main__':
    MainApp().run()
