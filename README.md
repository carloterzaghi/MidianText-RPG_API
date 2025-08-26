# Midian Text

Midian Text é uma API backend desenvolvida com **FastAPI** que gerencia funcionalidades essenciais para um jogo de RPG. Esta API permite o registro de usuários, login, gerenciamento de personagens e simulação de batalhas simples entre jogador e inimigo. Os dados são armazenados em um banco de dados **Firebase Firestore**, e as senhas são protegidas utilizando hash e salt via bcrypt.

## Instalação

### Pré-requisitos

- **Python 3.12+**
- Conta no **Firebase** e um projeto configurado no [Firebase Console](https://console.firebase.google.com/)
- Arquivo de credenciais do Firebase (`firebase.json`) na pasta `commands/keys`

### Dependências

Para instalar as dependências necessárias, execute:

```bash
pip install fastapi uvicorn firebase-admin bcrypt python-dotenv requests
```

## Execução da API

Para iniciar a API, execute o seguinte comando na raiz do projeto:

```bash
uvicorn main:app --reload
```

Esse comando inicia o servidor **Uvicorn** com recarregamento automático em [http://127.0.0.1:8000](http://127.0.0.1:8000).

Você pode acessar a documentação interativa dos endpoints em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

