# 🎮 MidianText RPG

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-1f538d?style=for-the-badge)

**RPG de Texto Moderno | Arquitetura Cliente-Servidor | Cloud Database**

*Sistema de Classes Balanceado • Combate Estratégico por Cores • Economia Persistente*

[Início Rápido](#-início-rápido) • [Documentação](#-como-funciona) • [API](#-endpoints-da-api) • [Mecânicas](#-mecânicas-de-jogo)

</div>

---

## 📋 O Que É Este Projeto?

**MidianText RPG** é um jogo completo de RPG desenvolvido em Python com:

- 🎯 **Backend RESTful** (FastAPI) + **Frontend Gráfico** (CustomTkinter)
- 🔐 **Autenticação JWT** + **Persistência Cloud** (Firebase Firestore)
- ⚔️ **4 Classes Balanceadas** + **Sistema de Cores Estratégico**
- 🛍️ **Loja com Economia** + **Sistema de Missões**
- 🚀 **Launcher Único** (`run.py`) que inicia tudo automaticamente

### 💡 Diferenciais Técnicos

- ✅ Arquitetura cliente-servidor profissional
- ✅ Separação clara de responsabilidades (Backend/Frontend)
- ✅ Processo de inicialização automatizado via `run.py`
- ✅ Validação de dados com Pydantic models
- ✅ Transações atômicas no Firebase
- ✅ Interface moderna com CustomTkinter

---

## 🚀 Início Rápido (3 Passos)

### 1️⃣ Instalar Dependências

```bash
# Clone o repositório
git clone https://github.com/carloterzaghi/MidianText-RPG_API.git
cd MidianText-RPG_API

# Instale as bibliotecas
pip install -r requirements.txt
```

### 2️⃣ Configurar Firebase

1. Crie projeto em: https://console.firebase.google.com/
2. Baixe credenciais: **Configurações** → **Contas de Serviço** → **Gerar Chave**
3. Salve como: `Backend - API/commands/keys/firebase.json`

### 3️⃣ Executar

```bash
# ⭐ Execute apenas este comando:
python run.py

# O que acontece:
# ✅ Backend inicia automaticamente (porta 8000)
# ✅ Aguarda 3s para estabilização
# ✅ Frontend abre em nova janela
# ✅ Pronto para jogar!
```

**Acesse a documentação da API**: http://127.0.0.1:8000/docs

---

## 🏗️ Como Funciona (Arquitetura)

### 📐 Diagrama Simplificado

```
┌─────────────────────────────────────────────────┐
│         🚀 run.py (LAUNCHER PRINCIPAL)          │
│  • Inicia Backend em processo separado          │
│  • Aguarda 3 segundos                           │
│  • Lança Frontend                               │
│  • Gerencia ciclo de vida                       │
└──────────────┬──────────────────┬───────────────┘
               │                  │
      ┌────────▼─────────┐  ┌────▼──────────┐
      │  BACKEND (API)   │  │ FRONTEND (GUI)│
      │  FastAPI:8000    │  │ CustomTkinter │
      └────────┬─────────┘  └────┬──────────┘
               │                  │
               │  HTTP REST API   │
               └─────────┬────────┘
                         │
              ┌──────────▼──────────┐
              │ FIREBASE FIRESTORE  │
              │ • usuarios          │
              │ • personagens       │
              │ • missions          │
              └─────────────────────┘
```

### 🔄 Fluxo de Execução (`run.py`)

**O `run.py` é o coração da aplicação**. Ele orquestra tudo:

```python
# 1. Localiza diretórios
project_root = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(project_root, "Backend - API")

# 2. Inicia Backend em background
api_process = subprocess.Popen([sys.executable, "main.py"], cwd=backend_dir)
time.sleep(3)  # ⏱️ Aguarda API ficar pronta

# 3. Verifica se API iniciou corretamente
if api_process.poll() is not None:
    print("❌ Erro ao iniciar API")
    return

# 4. Lança Frontend
subprocess.run('python Frontend/main.py', shell=True)

# 5. Mantém processos rodando
api_process.wait()

# 6. Trata Ctrl+C graciosamente
except KeyboardInterrupt:
    api_process.terminate()
```

**Por que `run.py`?**
- ✅ Sincronização garantida (backend pronto antes do frontend)
- ✅ Um único comando para executar tudo
- ✅ Encerramento gracioso (Ctrl+C termina ambos)
- ✅ Experiência de usuário profissional

---

## 📂 Estrutura do Código

```
MidianText-RPG_API/
│
├── 🚀 run.py                    # ⭐ EXECUTE ESTE ARQUIVO!
│
├── ⚙️ Backend - API/
│   ├── main.py                  # Servidor FastAPI (porta 8000)
│   │                            # • Registra rotas (login, personagens, missões)
│   │                            # • Configura CORS
│   │                            # • Inicia Uvicorn
│   │
│   └── commands/
│       ├── database.py          # Conexão Firebase
│       ├── func_senhas.py       # Bcrypt (hash de senhas)
│       ├── key_manager.py       # JWT tokens
│       │
│       ├── models/              # Pydantic (validação)
│       │   ├── user_model.py
│       │   ├── character_model.py
│       │   ├── items_table.py   # Catálogo da loja
│       │   │
│       │   └── classes/         # 4 Classes jogáveis
│       │       ├── assassino_class.py   # 🗡️ SPD + Crítico
│       │       ├── arqueiro_class.py    # 🏹 Alcance + Precisão
│       │       ├── mage_class.py        # 🔮 MAG + Controle
│       │       └── soldado_class.py     # 🛡️ HP + DEF
│       │
│       └── routes/              # Endpoints
│           ├── login.py         # POST /register, /login
│           ├── personagens.py   # CRUD de personagens
│           └── missions.py      # Sistema de missões
│
└── 🖥️ Frontend/
    ├── main.py                  # Interface CustomTkinter
    │                            # • App (controller)
    │                            # • LoginScreen
    │                            # • HomeScreen (gerenciar personagens)
    │                            # • GameScreen (jogar)
    │
    ├── api_client.py            # Cliente HTTP (requests)
    ├── shop.py                  # Janela da loja
    ├── missions.py              # Janela de missões
    └── character_creator.py     # Criador de personagens
```

---

## ⚔️ Mecânicas de Jogo

### 🎭 Classes de Personagem

Todas as classes herdam de `MainClasses` com atributos:

```python
hp_max   # Vida máxima
hp_tmp   # Vida atual
strg     # Força (dano físico)
mag      # Magia (dano mágico)
spd      # Velocidade (ordem de turno)
luck     # Sorte (chance de crítico)
defe     # Defesa (redução de dano)
mov      # Mobilidade (tiles por turno)
color    # Cor estratégica (vantagem em combate)
```

#### Comparativo de Classes

| Classe | HP | STR | MAG | SPD | DEF | Especialidade |
|--------|----|----|----|----|-----|---------------|
| 🗡️ Assassino | 80 | 12 | 5 | **15** | 6 | **Velocidade** + Críticos |
| 🏹 Arqueiro | 85 | 10 | 7 | 12 | 7 | **Alcance** + Precisão |
| 🔮 Mago | 70 | 5 | **18** | 8 | 5 | **Magia** + Controle |
| 🛡️ Soldado | **110** | 14 | 4 | 7 | **12** | **Tank** + Resistência |

### 🎨 Sistema de Cores (Vantagem Estratégica)

**Multiplicador de Dano: 1.5x**

```
🔴 Vermelho  →  VENCE  →  🟢 Verde
     ↑                         ↓
     |                       VENCE
   VENCE                       |
     |                         ↓
🔵 Azul      ←  VENCE  ←  🔴 Vermelho

⚫ Cinza = Neutro (sem bônus)
```

**Exemplo**:
```
Assassino 🔴 (STR 12) vs Mago 🟢 (DEF 5)
Dano Base: 12 - 5 = 7
Multiplicador: 1.5x (Vermelho > Verde)
Dano Final: 7 × 1.5 = 10.5 ≈ 11 HP
```

**Código (Simplificado)**:
```python
def calculate_color_advantage(attacker, defender):
    advantages = {
        "vermelho": "verde",
        "verde": "azul",
        "azul": "vermelho"
    }
    
    if advantages.get(attacker) == defender:
        return 1.5  # Vantagem
    elif advantages.get(defender) == attacker:
        return 0.67  # Desvantagem
    else:
        return 1.0  # Neutro
```

---

## 📡 Endpoints da API

### Base URL: `http://127.0.0.1:8000`

#### 🔐 Autenticação

**POST `/register`**
```json
Request:  {"username": "player1", "password": "senha123"}
Response: {"message": "Usuário criado com sucesso"}
```

**POST `/login`**
```json
Request:  {"username": "player1", "password": "senha123"}
Response: {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "username": "player1"
}
```

#### 🎭 Personagens

**GET `/personagens`** (Requer autenticação)
```
Headers: Authorization: Bearer <token>
Response: [
    {
        "id": "uuid",
        "name": "Aragorn",
        "character_class": "Soldado",
        "level": 1,
        "color": "vermelho",
        "gold": 100,
        "status": {...},
        "itens": {...},
        "habilidades": [...]
    }
]
```

**POST `/personagens/criar`**
```json
Headers: Authorization: Bearer <token>
Request: {
    "name": "Legolas",
    "character_class": "Arqueiro",
    "color": "verde"
}
Response: {
    "message": "Personagem criado",
    "character": {...}
}
```

**DELETE `/personagens/{name}`**
```
Headers: Authorization: Bearer <token>
Response: {"message": "Personagem deletado"}
```

#### 🛍️ Loja

**POST `/shop/buy`**
```json
Headers: Authorization: Bearer <token>
Request: {
    "character_name": "Aragorn",
    "item_name": "Poção de Cura",
    "quantity": 3
}
Response: {
    "message": "Comprado",
    "gold_remaining": 50,
    "item_quantity": 6
}
```

**POST `/shop/sell`**
```json
Request: {
    "character_name": "Aragorn",
    "item_name": "Poção de Cura",
    "quantity": 1
}
Response: {
    "message": "Vendido",
    "gold_earned": 25,  # 50% do preço
    "gold_total": 75
}
```

---

## 💾 Banco de Dados (Firebase)

### Estrutura Firestore

```json
{
  "usuarios": {
    "user_id_123": {
      "username": "player1",
      "password_hash": "$2b$12$...",
      "created_at": "2025-10-27"
    }
  },
  
  "personagens": {
    "user_id_123": {
      "personagens": [
        {
          "id": "uuid",
          "name": "Aragorn",
          "character_class": "Soldado",
          "level": 1,
          "color": "vermelho",
          "gold": 350,
          "exp": 0,
          
          "status": {
            "hp_max": 110,
            "hp_tmp": 110,
            "strg": 14,
            "mag": 4,
            "spd": 7,
            "luck": 6,
            "defe": 12,
            "mov": 5
          },
          
          "itens": {
            "Poção de Cura": 3,
            "Escudo de Ferro": 1,
            "Fuga": 1
          },
          
          "habilidades": [
            "Bloqueio Defensivo",
            "Contra-Ataque"
          ]
        }
      ]
    }
  },
  
  "missions": {
    "mission_001": {
      "name": "Floresta Sombria",
      "difficulty": "Fácil",
      "rewards": {"gold": 50, "exp": 100}
    }
  }
}
```

---

## 🛠️ Guia de Desenvolvimento

### Modificar uma Classe

**Exemplo: Aumentar HP do Mago**

```python
# Arquivo: Backend - API/commands/models/classes/mage_class.py

class Mago(MainClasses):
    def __init__(self):
        super().__init__()
        self.hp_max = 85  # Era 70, agora 85
        self.hp_tmp = 85
        # ... resto do código
```

### Adicionar Novo Item na Loja

```python
# Arquivo: Backend - API/commands/models/items_table.py

class ItemTable:
    ITEMS = {
        # ... itens existentes ...
        
        "Espada Flamejante": {
            "type": "Arma",
            "price": 500,
            "effect": {"strg": 8, "fire_damage": 10},
            "class_restriction": "Soldado"  # ou None
        }
    }
```

### Criar Nova Rota (Endpoint)

```python
# Arquivo: Backend - API/commands/routes/personagens.py

@router.get("/personagens/{character_name}/inventory")
def get_inventory(character_name: str, authorization: str = Header(None)):
    # 1. Verificar token
    user_id = verify_key(token)
    
    # 2. Buscar personagem
    personagens_doc = personagens_collection.document(user_id).get()
    personagens = personagens_doc.to_dict().get("personagens", [])
    
    # 3. Encontrar personagem específico
    character = next((p for p in personagens if p["name"] == character_name), None)
    
    # 4. Retornar inventário
    return {"inventory": character.get("itens", {})}
```

Não esqueça de registrar no `main.py`:
```python
# Backend - API/main.py
from commands.routes.personagens import router as personagens_router
app.include_router(personagens_router)
```

---

## 🐛 Solução de Problemas

### ❌ Erro: "Não consegue conectar à API"

**Sintoma**: Frontend não abre ou não carrega personagens

**Soluções**:
```bash
# 1. Verificar se backend está rodando
# Abra http://127.0.0.1:8000/docs no navegador
# Deve ver documentação Swagger

# 2. Verificar porta 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                  # Linux/Mac

# 3. Reiniciar tudo
# Ctrl+C para fechar
python run.py  # Rodar novamente
```

### ❌ Erro: "Firebase credentials not found"

**Sintoma**: API não inicia, erro de credenciais

**Solução**:
```bash
# Verificar se arquivo existe
ls "Backend - API/commands/keys/firebase.json"

# Deve mostrar o arquivo. Se não:
# 1. Baixe novamente do Firebase Console
# 2. Coloque na pasta correta
# 3. Renomeie para "firebase.json"
```

### ❌ Erro: "Token inválido ou expirado"

**Sintoma**: Após algum tempo, pede login novamente

**Explicação**: Tokens JWT expiram em 30 minutos (segurança)

**Solução**: Faça login novamente (comportamento esperado)

### ❌ Erro: "Já existe 3 personagens"

**Sintoma**: Não consegue criar mais personagens

**Explicação**: Limite de 3 personagens por usuário (regra de jogo)

**Solução**: Delete um personagem existente antes de criar novo

---

## 🚀 Roadmap (Futuro)

### ✅ Implementado
- [x] Sistema de autenticação JWT
- [x] CRUD de personagens (limite de 3)
- [x] 4 classes balanceadas
- [x] Sistema de cores (vantagem de combate)
- [x] Loja com economia persistente
- [x] Inventário completo
- [x] Confirmação de exclusão
- [x] Launcher automatizado (`run.py`)

### 🔄 Em Desenvolvimento
- [ ] Sistema de combate tático em grid
- [ ] Missões com narrativa
- [ ] Crafting de itens

### 📋 Planejado
- [ ] Modo multiplayer (PvP/Co-op)
- [ ] Sistema de guildas
- [ ] Mais classes (Necromante, Paladino)
- [ ] Sistema de pets
- [ ] Eventos temporários
- [ ] Ranking global

---

## 👤 Créditos

**Desenvolvido por**: Carlo Terzaghi  
**GitHub**: [@carloterzaghi](https://github.com/carloterzaghi)  
**Licença**: Proprietário © 2025  

### Tecnologias Utilizadas

- **FastAPI** - Framework web moderno
- **CustomTkinter** - Interface gráfica clean
- **Firebase** - Database em nuvem
- **Bcrypt** - Segurança de senhas
- **JWT** - Autenticação stateless

### Agradecimentos

- Comunidade Python Brasil
- Equipe FastAPI
- Desenvolvedores CustomTkinter
- Firebase Team
- Beta Testers

---

<div align="center">

**⚔️ Bem-vindo ao mundo de Midian! ⚔️**

Desenvolvido com ❤️ em Python

**Última Atualização**: 27 de Outubro de 2025  
**Versão**: 1.0.0

</div>
