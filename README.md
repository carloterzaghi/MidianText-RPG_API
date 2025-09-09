# Midian Text RPG

Midian Text é uma API backend desenvolvida com **FastAPI** para gerenciar funcionalidades essenciais de um jogo de RPG.  
Permite registro e login de usuários, gerenciamento de personagens e simulação de batalhas simples.  
Os dados são armazenados no **Firebase Firestore** e as senhas são protegidas com hash e salt via bcrypt.

## Instalação

### Pré-requisitos

- **Python 3.12+**
- Conta no **Firebase** e projeto criado no [Firebase Console](https://console.firebase.google.com/)
- Arquivo de credenciais do Firebase (`firebase.json`) na pasta `Backend - API/commands/keys`
- Arquivo `.env` na raiz do projeto, contendo sua chave secreta:
  ```
  SECRET_KEY=sua-chave-secreta-aqui
  ```

### Dependências

Instale as dependências com:

```bash
pip install -r requirements.txt
```

## Execução da API e Frontend

Para iniciar a API e o frontend juntos, execute:

```bash
python run.py
```

Ou, para rodar manualmente:

**Backend:**
```bash
uvicorn "Backend - API/main:app" --reload
```

**Frontend (terminal):**
```bash
python Frontend/main.py
```

Acesse a documentação interativa dos endpoints em:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Estrutura do Projeto

```
MidianText-RPG_API/
│
├── Backend - API/
│   ├── main.py
│   ├── commands/
│   │   ├── database.py
│   │   ├── func_senhas.py
│   │   ├── key_manager.py
│   │   ├── keys/
│   │   │   └── firebase.json
│   │   └── models/
│   │       ├── character_model.py
│   │       └── user_model.py
│   │   └── routes/
│   │       ├── login.py
│   │       └── personagens.py
│
├── Frontend/
│   └── main.py
│
├── requirements.txt
├── run.py
└── README.md
```

## Observações

- O token gerado no login é temporário (expira em 30 minutos) e garante que cada usuário só acesse seus próprios dados.
- Mantenha sua chave secreta (`SECRET_KEY`) protegida e nunca compartilhe o arquivo `firebase.json`

