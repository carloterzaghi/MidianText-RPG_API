"""
MidianText RPG - Configuração do Banco de Dados Firebase
==========================================================

Este módulo gerencia a conexão com o Firebase Firestore, o banco de dados NoSQL
em nuvem utilizado para armazenar todos os dados do jogo.

Funcionalidades:
    - Inicialização do Firebase Admin SDK
    - Configuração do cliente Firestore
    - Definição das collections principais

Collections Disponíveis:
    - usuarios_collection: Armazena dados de autenticação dos usuários
    - personagens_collection: Armazena personagens criados pelos usuários

Estrutura de Dados:
    usuarios/{user_id}:
        - username: str
        - salt: str (para hashing de senha)
        - password: str (hash da senha)
    
    personagens/{user_id}:
        - user_id: str
        - personagens: List[dict] (lista de até 3 personagens)

Segurança:
    - Credenciais Firebase em arquivo separado (não versionado)
    - Acesso controlado via Firebase Admin SDK
    - Validação de permissões no lado do servidor

Dependencies: firebase-admin
"""

import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa o Firebase Admin SDK com as credenciais do projeto
# Arquivo firebase.json deve estar em commands/keys/ (não commitar!)
cred = credentials.Certificate("commands/keys/firebase.json")
firebase_admin.initialize_app(cred)

# Cliente Firestore para interação com o banco de dados
db = firestore.client()

# Collections principais do sistema
usuarios_collection = db.collection("usuarios")  # Autenticação e dados de usuários
personagens_collection = db.collection("personagens")  # Personagens dos usuários
