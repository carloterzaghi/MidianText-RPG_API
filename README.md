# 🎮 MidianText RPG

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![Firebase](https://img.shields.io/badge/Firebase-Firestore-orange.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)

**Um RPG de texto moderno com interface gráfica e arquitetura cliente-servidor**

[Características](#-características-principais) • [Instalação](#-instalação) • [Uso](#-guia-de-uso) • [API](#-api-reference) • [Sistemas](#-sistemas-de-jogo)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Características Principais](#-características-principais)
- [Arquitetura do Sistema](#️-arquitetura-do-sistema)
- [Stack Tecnológico](#-stack-tecnológico)
- [Instalação](#-instalação)
- [Guia de Uso](#-guia-de-uso)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Sistemas de Jogo](#-sistemas-de-jogo)
- [API Reference](#-api-reference)
- [Banco de Dados](#-estrutura-do-banco-de-dados)
- [Troubleshooting](#-troubleshooting)
- [Roadmap](#-roadmap)
- [Autor](#-autor)

---

## 🎯 Visão Geral

**MidianText RPG** é um jogo de RPG baseado em texto com interface gráfica moderna, desenvolvido em Python. O projeto utiliza uma arquitetura cliente-servidor robusta, onde o backend gerencia toda a lógica de negócio e persistência de dados no Firebase Firestore, enquanto o frontend fornece uma experiência visual rica e intuitiva através do CustomTkinter.

### 🌟 Características Principais

- ✅ **Sistema de Autenticação Seguro**: JWT-based authentication com tokens temporários
- ✅ **Gerenciamento de Personagens**: CRUD completo com limite de 3 personagens por usuário
- ✅ **4 Classes Únicas**: Assassino, Arqueiro, Mago e Soldado - cada um com stats e habilidades exclusivas
- ✅ **Sistema de Cores Estratégico**: Mecânica tipo pedra-papel-tesoura com vantagens de combate (1.5x dano)
- ✅ **Sistema de Missões**: Missões com mapas, inimigos e recompensas dinâmicas
- ✅ **Loja Integrada**: Compra e venda de itens com economia persistente
- ✅ **Persistência Cloud**: Todos os dados salvos em tempo real no Firebase Firestore
- ✅ **Interface Moderna**: CustomTkinter com design clean e responsivo
- ✅ **Sistema de Inventário**: Gerenciamento completo de itens e equipamentos
- ✅ **Exclusão com Confirmação**: Proteção contra deleção acidental de personagens

---

## 🏗️ Arquitetura do Sistema

```
┌─────────────────────────┐
│   Frontend (GUI)        │ ← CustomTkinter + Requests
│   • Telas de Login      │
│   • Gerenciamento Chars │
│   • Loja e Missões      │
└───────────┬─────────────┘
            │ HTTP/REST API
            ↓
┌─────────────────────────┐
│   API Client Module     │ ← Camada de Comunicação
│   • Authentication      │
│   • Character CRUD      │
│   • Shop & Missions     │
└───────────┬─────────────┘
            │ HTTP Requests
            ↓
┌─────────────────────────┐
│   FastAPI Backend       │ ← Servidor Web ASGI
│   • JWT Validation      │
│   • Business Logic      │
│   • Data Validation     │
└───────────┬─────────────┘
            │ Firebase Admin SDK
            ↓
┌─────────────────────────┐
│   Firebase Firestore    │ ← Cloud NoSQL Database
│   • Users Collection    │
│   • Characters Data     │
│   • Missions State      │
└─────────────────────────┘
```

### 📊 Fluxo de Dados

1. **Usuário interage** com a interface gráfica (CustomTkinter)
2. **Frontend solicita** dados via `api_client.py` (camada de abstração)
3. **API Client envia** requisição HTTP/REST autenticada para o backend
4. **FastAPI valida** JWT token e dados com Pydantic models
5. **Backend processa** lógica de negócio (validações, cálculos, regras)
6. **Firebase persiste/busca** dados no Firestore (transações atômicas)
7. **Backend retorna** resposta JSON estruturada
8. **Frontend atualiza** UI em tempo real com os dados recebidos

---

## 🛠️ Stack Tecnológico

### Backend
| Tecnologia | Versão | Função |
|-----------|--------|--------|
| **Python** | 3.8+ | Linguagem principal |
| **FastAPI** | 0.104+ | Framework web moderno e rápido |
| **Uvicorn** | 0.24+ | Servidor ASGI de alta performance |
| **Firebase Admin SDK** | 6.2+ | Integração com Firestore Database |
| **Pydantic** | 2.4+ | Validação de dados e serialização |
| **python-jose** | 3.3+ | Geração e validação de JWT tokens |
| **passlib** | 1.7+ | Hashing de senhas com bcrypt |

### Frontend
| Tecnologia | Versão | Função |
|-----------|--------|--------|
| **Python** | 3.8+ | Linguagem principal |
| **CustomTkinter** | 5.2+ | Framework GUI moderno |
| **Requests** | 2.31+ | Cliente HTTP para API REST |
| **Pillow** | 10.1+ | Processamento de imagens |

---

## 📥 Instalação

### Pré-requisitos

- ✅ **Python 3.8 ou superior** instalado
- ✅ **pip** (gerenciador de pacotes Python)
- ✅ **Conta Firebase** com projeto configurado
- ✅ **Conexão com internet** (para Firebase)

### Passo a Passo

#### 1️⃣ Clone o Repositório

```bash
git clone https://github.com/carloterzaghi/MidianText-RPG_API.git
cd MidianText-RPG_API
```

#### 2️⃣ Instale as Dependências

```bash
pip install -r requirements.txt
```

**Dependências incluídas**:
```
fastapi==0.104.1
uvicorn==0.24.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
firebase-admin==6.2.0
pydantic==2.4.2
requests==2.31.0
customtkinter==5.2.0
pillow==10.1.0
```

#### 3️⃣ Configure o Firebase

1. Acesse o [Firebase Console](https://console.firebase.google.com/)
2. Crie um novo projeto ou use um existente
3. Vá em **Project Settings** → **Service Accounts**
4. Clique em **Generate New Private Key**
5. Salve o arquivo JSON em `Backend - API/commands/keys/`
6. Renomeie para `firebase.json`

#### 4️⃣ Configure Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-jwt-aqui
TOKEN_EXPIRATION=30
```

#### 5️⃣ Execute a Aplicação

**Opção 1: Launcher Automático (Recomendado)**
```bash
python run.py
```

**Opção 2: Execução Manual**
```bash
# Terminal 1 - Backend
cd "Backend - API"
python main.py

# Terminal 2 - Frontend
cd Frontend
python main.py
```

#### 6️⃣ Acesse a Documentação Interativa

Abra seu navegador em: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📖 Guia de Uso

### 🎮 Primeira Execução

#### **1. Registre um Usuário**
- Clique em **"Registrar"** na tela de login
- Escolha um **username** (2-20 caracteres alfanuméricos)
- Crie uma **senha** (mínimo 6 caracteres)
- Confirme o registro

#### **2. Faça Login**
- Insira suas credenciais
- Sistema gerará um **JWT token** (válido por 30 minutos)
- Você será redirecionado para a **Home Screen**

#### **3. Crie seu Primeiro Personagem**
- Clique em **"⚔️ Criar Novo Personagem"**
- Escolha um **nome único** para seu personagem
- Selecione uma **classe** (veja stats e habilidades)
- Escolha uma **cor estratégica** (vantagem em combate)
- Confirme a criação

#### **4. Explore o Jogo**
- **Ver Detalhes**: Visualize stats completos do personagem
- **Acessar Loja**: Compre e venda itens
- **Fazer Missões**: Complete objetivos e ganhe recompensas
- **Gerenciar Inventário**: Organize seus itens

### 🛡️ Limites e Restrições

| Limite | Valor | Observação |
|--------|-------|------------|
| **Personagens por Usuário** | 3 | Máximo permitido |
| **Nome de Personagem** | Único | Por usuário |
| **Token JWT** | 30 min | Tempo de expiração |
| **Exclusão de Personagem** | Confirmação obrigatória | Proteção contra acidentes |

---

## 📁 Estrutura do Projeto

```
MidianText-RPG_API/
│
├── run.py                          # 🚀 Launcher principal (inicia backend + frontend)
├── README.md                       # 📖 Documentação do projeto
├── requirements.txt                # 📦 Dependências Python
│
├── Backend - API/                  # ⚙️ Servidor FastAPI
│   ├── main.py                     # Aplicação principal FastAPI
│   │
│   └── commands/
│       ├── database.py             # Configuração Firebase Firestore
│       ├── func_senhas.py          # Hashing bcrypt para senhas
│       ├── key_manager.py          # Gerenciamento de JWT tokens
│       ├── missions_data.py        # Dados de missões e NPCs
│       │
│       ├── keys/
│       │   └── firebase.json       # 🔑 Credenciais Firebase (NÃO COMMITAR!)
│       │
│       ├── models/                 # 📋 Modelos Pydantic
│       │   ├── user_model.py
│       │   ├── character_model.py
│       │   ├── character_creation_model.py
│       │   ├── mission_model.py
│       │   ├── items_table.py
│       │   │
│       │   └── classes/            # Classes de personagem
│       │       ├── _main_classes.py
│       │       ├── assassino_class.py
│       │       ├── arqueiro_class.py
│       │       ├── mage_class.py
│       │       └── soldado_class.py
│       │
│       └── routes/                 # 🛤️ Endpoints da API
│           ├── login.py            # Autenticação (register/login)
│           ├── personagens.py      # CRUD de personagens
│           └── missions.py         # Sistema de missões
│
└── Frontend/                       # 🖥️ Interface Gráfica
    ├── main.py                     # Aplicação principal GUI
    ├── api_client.py               # Cliente HTTP para API
    ├── shop.py                     # Janela da loja
    ├── missions.py                 # Janela de missões
    └── character_creator.py        # Criador de personagens
```

---

## ⚔️ Sistemas de Jogo

### 🎭 Classes de Personagem

#### **🗡️ Assassino**
```
Especialista em velocidade e ataques críticos letais

📊 Stats Base:
├─ HP: 80    │ ❤️ Vida moderada
├─ STR: 12   │ ⚔️ Ataque médio
├─ MAG: 5    │ ✨ Magia baixa
├─ SPD: 15   │ ⚡ Velocidade alta
├─ LUCK: 12  │ 🍀 Sorte alta (críticos)
├─ DEF: 6    │ 🛡️ Defesa baixa
└─ MOV: 8    │ 👣 Mobilidade alta

💥 Habilidades:
• Ataque Furtivo - Dano crítico aumentado
• Evasão Crítica - Esquiva aprimorada

🎒 Item Inicial: Adagas Gêmeas (+5 STR, Chance de Crítico)
```

#### **🏹 Arqueiro**
```
Mestre do combate à distância e precisão mortal

📊 Stats Base:
├─ HP: 85    │ ❤️ Vida moderada
├─ STR: 10   │ ⚔️ Ataque médio
├─ MAG: 7    │ ✨ Magia baixa
├─ SPD: 12   │ ⚡ Velocidade boa
├─ LUCK: 10  │ 🍀 Sorte moderada
├─ DEF: 7    │ 🛡️ Defesa baixa
└─ MOV: 7    │ 👣 Mobilidade média

🎯 Habilidades:
• Tiro Preciso - Acerto garantido
• Flecha Múltipla - Ataque em área

🎒 Item Inicial: Arco Élfico (+4 STR, Alcance Aumentado)
```

#### **🔮 Mago**
```
Dominador das artes arcanas e feitiços devastadores

📊 Stats Base:
├─ HP: 70    │ ❤️ Vida baixa
├─ STR: 5    │ ⚔️ Ataque baixo
├─ MAG: 18   │ ✨ Magia muito alta
├─ SPD: 8    │ ⚡ Velocidade baixa
├─ LUCK: 8   │ 🍀 Sorte moderada
├─ DEF: 5    │ 🛡️ Defesa muito baixa
└─ MOV: 6    │ 👣 Mobilidade baixa

✨ Habilidades:
• Bola de Fogo - Dano mágico em área
• Escudo Arcano - Proteção mágica

🎒 Item Inicial: Cajado Arcano (+6 MAG, Reduz Custo de Mana)
```

#### **🛡️ Soldado**
```
Tanque resistente e protetor do grupo

📊 Stats Base:
├─ HP: 110   │ ❤️ Vida muito alta
├─ STR: 14   │ ⚔️ Ataque alto
├─ MAG: 4    │ ✨ Magia muito baixa
├─ SPD: 7    │ ⚡ Velocidade baixa
├─ LUCK: 6   │ 🍀 Sorte baixa
├─ DEF: 12   │ 🛡️ Defesa muito alta
└─ MOV: 5    │ 👣 Mobilidade muito baixa

🛡️ Habilidades:
• Bloqueio Defensivo - Reduz dano recebido
• Contra-Ataque - Revida após bloqueio

🎒 Item Inicial: Escudo de Ferro (+4 DEF, Redução de Dano)
```

---

### 🎨 Sistema de Cores (Vantagem de Combate)

```
        🔴 VERMELHO
         /       \
        /         \
    vence        perde
      /             \
     ↓               ↓
🟢 VERDE ─────────> 🔵 AZUL
           vence

⚫ CINZA = Neutro (sem vantagens)
```

**📐 Multiplicador de Vantagem: 1.5x de dano**

| Atacante | vs | Defensor | Resultado |
|----------|---|----------|-----------|
| 🔴 Vermelho | → | 🟢 Verde | **150% de dano** |
| 🟢 Verde | → | 🔵 Azul | **150% de dano** |
| 🔵 Azul | → | 🔴 Vermelho | **150% de dano** |
| ⚫ Cinza | → | Qualquer | **100% de dano** (neutro) |

**💡 Dica Estratégica**: Escolha a cor do seu personagem pensando nos inimigos que você enfrentará!

---

### 🎒 Sistema de Itens

#### **Itens Iniciais** (Todo personagem começa com)
- 🧪 **Poção de Cura** x3 - Restaura 30 HP
- 📜 **Fuga** x1 - Permite escapar de batalha

#### **Catálogo da Loja**

**💊 Consumíveis**
| Item | Preço | Efeito | Venda |
|------|-------|--------|-------|
| 🧪 Poção de Cura | 50 🪙 | +25 HP | 25 🪙 |
| 🧪 Poção Grande | 120 🪙 | +50 HP | 60 🪙 |
| 📜 Fuga | 100 🪙 | Escapar de batalha | 50 🪙 |
| 💪 Elixir de Força | 80 🪙 | +5 STR (temp) | 40 🪙 |
| ✨ Elixir de Magia | 80 🪙 | +5 MAG (temp) | 40 🪙 |

**⚔️ Armas (Específicas por Classe)**
| Item | Classe | Preço | Bônus | Venda |
|------|--------|-------|-------|-------|
| 🗡️ Adagas Gêmeas | Assassino | 300 🪙 | +5 STR, Crítico | 150 🪙 |
| 🏹 Arco Élfico | Arqueiro | 350 🪙 | +4 STR, Alcance | 175 🪙 |
| 🔮 Cajado Arcano | Mago | 400 🪙 | +6 MAG, -Mana | 200 🪙 |

**🛡️ Armaduras**
| Item | Classe | Preço | Bônus | Venda |
|------|--------|-------|-------|-------|
| 🛡️ Escudo de Ferro | Soldado | 250 🪙 | +4 DEF, -Dano | 125 🪙 |

**💰 Economia**
- Cada personagem **inicia com 100 moedas de ouro**
- Itens vendidos rendem **50% do valor original**
- Todas as transações são **persistidas no Firebase** em tempo real

---

### 🛍️ Como Usar a Loja

1. **Acesse a Loja**: No menu do jogo, clique em **🛍️ Loja**
2. **Navegue pelos Itens**: Use filtros (Todos, Consumível, Arma, Armadura)
3. **Compre Itens**: 
   - Selecione o item desejado
   - Clique em **🛒 Comprar**
   - Confirme a transação
4. **Venda Itens**:
   - Acesse seu **Inventário** (lado direito)
   - Selecione o item para vender
   - Clique em **💸 Vender**
   - Receba 50% do valor

**⚠️ Validações Automáticas**:
- ✅ Verificação de ouro suficiente
- ✅ Restrições de classe para equipamentos
- ✅ Verificação de estoque no inventário
- ✅ Transações atômicas no Firebase

---

## 🔌 API Reference

### 🔐 Autenticação

#### **POST** `/register`
Registra um novo usuário no sistema.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (201 Created):**
```json
{
  "message": "Usuário criado com sucesso"
}
```

---

#### **POST** `/login`
Autentica usuário e retorna JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "username": "string"
}
```

---

### 🎭 Personagens

#### **GET** `/personagens`
Lista todos os personagens do usuário autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "id": "uuid-v4",
    "name": "Aragorn",
    "character_class": "Soldado",
    "level": 5,
    "color": "vermelho",
    "gold": 350,
    "exp": 1250,
    "status": {
      "hp_max": 110,
      "hp_atual": 95,
      "strg": 14,
      "mag": 4,
      "spd": 7,
      "luck": 6,
      "defe": 12,
      "mov": 5
    },
    "itens": {
      "Poção de Cura": 3,
      "Escudo de Ferro": 1
    },
    "habilidades": [
      "Bloqueio Defensivo",
      "Contra-Ataque"
    ]
  }
]
```

---

#### **POST** `/personagens/criar`
Cria um novo personagem (máximo 3 por usuário).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Legolas",
  "character_class": "Arqueiro",
  "color": "verde"
}
```

**Response (201 Created):**
```json
{
  "message": "Personagem criado com sucesso",
  "character": {
    "id": "uuid-v4",
    "name": "Legolas",
    "character_class": "Arqueiro",
    "level": 1,
    "color": "verde",
    "gold": 100,
    ...
  }
}
```

---

#### **DELETE** `/personagens/{character_name}`
Deleta um personagem específico.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "message": "Personagem 'Legolas' deletado com sucesso"
}
```

---

#### **GET** `/personagens/classes`
Retorna informações de todas as classes disponíveis.

**Response (200 OK):**
```json
{
  "Assassino": {
    "name": "Assassino",
    "description": "Especialista em velocidade e ataques críticos",
    "stats": {
      "hp_max": 80,
      "strg": 12,
      "mag": 5,
      ...
    },
    "habilidades": ["Ataque Furtivo", "Evasão Crítica"]
  },
  ...
}
```

---

### 🛍️ Loja

#### **GET** `/shop/items`
Lista todos os itens disponíveis na loja.

**Response (200 OK):**
```json
[
  {
    "name": "Poção de Cura",
    "type": "Consumível",
    "price": 50,
    "effect": "Restaura 25 HP",
    "class_restriction": null
  },
  ...
]
```

---

#### **POST** `/shop/buy`
Compra um item da loja.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "character_name": "Aragorn",
  "item_name": "Poção de Cura",
  "quantity": 3
}
```

**Response (200 OK):**
```json
{
  "message": "Item comprado com sucesso",
  "gold_remaining": 250,
  "item_quantity": 6
}
```

---

#### **POST** `/shop/sell`
Vende um item do inventário (50% do valor).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "character_name": "Aragorn",
  "item_name": "Poção de Cura",
  "quantity": 1
}
```

**Response (200 OK):**
```json
{
  "message": "Item vendido com sucesso",
  "gold_earned": 25,
  "gold_total": 275
}
```

---

#### **GET** `/personagens/{character_name}/gold`
Retorna o ouro atual do personagem.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "character_name": "Aragorn",
  "gold": 350
}
```

---

### 🗺️ Missões

#### **GET** `/missions`
Lista todas as missões disponíveis.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "missions": [
    {
      "id": "mission_001",
      "name": "Floresta Sombria",
      "difficulty": "Fácil",
      "rewards": {
        "gold": 50,
        "exp": 100
      }
    },
    ...
  ]
}
```

---

#### **POST** `/missions/start`
Inicia uma missão com um personagem.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "character_name": "Aragorn",
  "mission_id": "mission_001"
}
```

---

#### **POST** `/missions/action`
Executa uma ação durante a missão.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "character_name": "Aragorn",
  "mission_id": "mission_001",
  "action": "move|fight|collect|flee",
  "target": "enemy_goblin"
}
```

---

### 📊 Status Codes

| Código | Significado | Uso |
|--------|-------------|-----|
| **200** | OK | Requisição bem-sucedida |
| **201** | Created | Recurso criado com sucesso |
| **400** | Bad Request | Dados inválidos ou ausentes |
| **401** | Unauthorized | Token inválido ou ausente |
| **404** | Not Found | Recurso não encontrado |
| **409** | Conflict | Conflito (ex: nome duplicado) |
| **500** | Internal Server Error | Erro no servidor |

---

## 💾 Estrutura do Banco de Dados

### Firebase Firestore Schema

```json
{
  "users": {
    "username_123": {
      "username": "JogadorPro",
      "password_hash": "$2b$12$...",
      "created_at": "2025-10-26T10:30:00Z",
      
      "personagens": {
        "Aragorn": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "name": "Aragorn",
          "character_class": "Soldado",
          "level": 5,
          "color": "vermelho",
          "gold": 350,
          "exp": 1250,
          
          "status": {
            "hp_max": 110,
            "hp_atual": 95,
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
          ],
          
          "created_at": "2025-10-20T15:45:00Z"
        },
        
        "Legolas": {
          "id": "650e8400-e29b-41d4-a716-446655440001",
          "name": "Legolas",
          "character_class": "Arqueiro",
          ...
        }
      }
    }
  },
  
  "missions": {
    "mission_001": {
      "name": "Floresta Sombria",
      "difficulty": "Fácil",
      "map": [...],
      "enemies": [...],
      "rewards": {
        "gold": 50,
        "exp": 100
      }
    }
  }
}
```

---

## 🐛 Troubleshooting

### ❌ Erro: "Não é possível conectar à API"

**Sintomas**: Frontend não consegue se comunicar com o backend

**Causas Possíveis**:
- Backend não está rodando
- Porta 8000 está ocupada
- Firewall bloqueando conexão

**Soluções**:
```bash
# Verifique se o backend está rodando
cd "Backend - API"
python main.py

# Verifique se a porta 8000 está livre (Windows)
netstat -ano | findstr :8000

# Teste a conexão
curl http://127.0.0.1:8000/
```

---

### ❌ Erro: "Token inválido ou expirado"

**Sintomas**: Requisições retornam 401 Unauthorized

**Causas Possíveis**:
- JWT token expirou (30 minutos)
- Token corrompido ou inválido

**Soluções**:
1. Faça **logout** e **login** novamente
2. Verifique se a `SECRET_KEY` é a mesma no servidor
3. Limpe o cache e reinicie a aplicação

---

### ❌ Erro ao Inicializar Firebase

**Sintomas**: 
```
firebase_admin.exceptions.InvalidArgumentError: 
Could not load credentials
```

**Causas Possíveis**:
- Arquivo `firebase.json` não encontrado
- Caminho incorreto
- Permissões de arquivo

**Soluções**:
```bash
# Verifique se o arquivo existe
ls "Backend - API/commands/keys/firebase.json"

# Verifique permissões (Linux/Mac)
chmod 644 "Backend - API/commands/keys/firebase.json"

# Valide o JSON
python -m json.tool "Backend - API/commands/keys/firebase.json"
```

---

### ❌ Personagem Não Aparece Após Criação

**Sintomas**: Personagem criado mas não aparece na lista

**Causas Possíveis**:
- Problema de sincronização
- Cache do frontend
- Erro na persistência

**Soluções**:
1. Clique no botão **Recarregar** (se disponível)
2. Faça **logout** e **login** novamente
3. Verifique no **Firebase Console** se os dados foram salvos
4. Verifique logs do backend para erros

---

### ❌ Botões Não Aparecem em Diálogos

**Sintomas**: Janelas de confirmação sem botões visíveis

**Status**: ✅ **CORRIGIDO** na versão atual

**Detalhes**: Layout simplificado usando `pack()` ao invés de `grid()` com frames transparentes.

---

### 🔍 Ativando Logs de Debug

**Backend:**
```python
# Backend - API/main.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        log_level="debug"  # ← Ativa logs detalhados
    )
```

**Frontend:**
```python
# Frontend/main.py
# Adicione prints estratégicos
print(f"[DEBUG] Token: {self.controller.access_token}")
print(f"[DEBUG] Personagens carregados: {personagens}")
print(f"[DEBUG] Ouro atual: {gold}")
```

---

## 🚀 Roadmap

### ✅ Implementado
- [x] Sistema de autenticação JWT
- [x] CRUD completo de personagens
- [x] 4 classes balanceadas
- [x] Sistema de cores estratégico
- [x] Loja com economia persistente
- [x] Sistema de inventário
- [x] Exclusão de personagens com confirmação
- [x] Interface gráfica moderna

### 🔄 Em Desenvolvimento
- [ ] Sistema de combate em tempo real
- [ ] Missões com narrativa expandida
- [ ] Sistema de crafting de itens
- [ ] Achievements e conquistas

### 📋 Planejado
- [ ] Modo multiplayer (PvP e Co-op)
- [ ] Sistema de guildas
- [ ] Mais classes (Necromante, Paladino, Druida)
- [ ] Sistema de pets e montarias
- [ ] Ranking global de jogadores
- [ ] Eventos temporários e sazonais
- [ ] Sistema de trading entre jogadores
- [ ] Modo história com cutscenes

### 💭 Em Consideração
- [ ] Versão web (React + TypeScript)
- [ ] Aplicativo mobile (React Native)
- [ ] Integração com Discord
- [ ] Sistema de moedas premium
- [ ] Modo Battle Royale
- [ ] API pública para desenvolvedores

---

## 📄 Licença

Este projeto é **proprietário** e de uso exclusivo do autor.  
**Todos os direitos reservados © 2025 Carlo Terzaghi**

---

## 👤 Autor

**Carlo Terzaghi**  
GitHub: [@carloterzaghi](https://github.com/carloterzaghi)  
📧 Email: Disponível mediante solicitação

---

## 🙏 Agradecimentos

- 🐍 **Comunidade Python Brasil** - Suporte e inspiração
- ⚡ **Equipe FastAPI** - Framework incrível
- 🎨 **Desenvolvedores CustomTkinter** - GUI moderna
- 🔥 **Firebase Team** - Cloud database confiável
- 🧪 **Beta Testers** - Feedback valioso

---

## 📞 Suporte

Encontrou um bug? Tem uma sugestão? 

1. 🐛 **Issues**: [Abra uma issue](https://github.com/carloterzaghi/MidianText-RPG_API/issues)
2. 💬 **Discussões**: [Inicie uma discussão](https://github.com/carloterzaghi/MidianText-RPG_API/discussions)
3. 📧 **Email**: Entre em contato diretamente

---

<div align="center">

**⚔️ Bem-vindo ao mundo de Midian! ⚔️**

Desenvolvido com ❤️ por Carlo Terzaghi

**Última Atualização**: 26 de Outubro de 2025  
**Versão**: 1.0.0

</div>
├── requirements.txt
├── run.py
└── README.md
```

## Funcionalidades

### Backend (API)
- ✅ Registro e autenticação de usuários com JWT
- ✅ Criação e gerenciamento de personagens (máximo 3 por usuário)
- ✅ Sistema de classes (Assassino, Arqueiro, Mago, Soldado)
- ✅ Sistema de cores com vantagens de combate
- ✅ Catálogo de itens (armas, armaduras, consumíveis)
- 🔄 Sistema de loja (em implementação)
- 🔄 Sistema de combate (em desenvolvimento)

### Frontend (Interface Gráfica)
- ✅ Tela de Login e Registro
- ✅ Gerenciamento de personagens
- ✅ Criação de personagens com preview de stats
- ✅ **Loja do Jogo** - Sistema completo integrado!
  - 🛒 Compra de itens (persistido no Firebase)
  - 💰 Sistema de ouro (atualizado em tempo real)
  - 🎒 Visualização de inventário
  - 💸 Venda de itens (50% do valor original)
  - 🔍 Filtros por tipo (Consumível, Arma, Armadura)
  - ⚔️ Restrições por classe para equipamentos
  - ✅ **Transações persistidas no Firebase!**
- 🔄 Sistema de missões (em desenvolvimento)

### Como usar a Loja

1. Faça login e selecione um personagem
2. No menu do jogo, clique em **🛍️ Loja**
3. Na loja você pode:
   - **Comprar itens**: Selecione um item e clique em "🛒 Comprar"
   - **Vender itens**: Vá até seu inventário (lado direito) e clique em "💸 Vender"
   - **Filtrar itens**: Use o menu de filtros para ver apenas consumíveis, armas ou armaduras
4. Cada personagem começa com **100 moedas de ouro** ao ser criado

### Itens Disponíveis na Loja

**Consumíveis:**
- 🧪 Poção de Cura (50 ouro) - Restaura 25 HP
- 🧪 Poção Grande de Cura (120 ouro) - Restaura 50 HP
- 📜 Fuga (100 ouro) - Permite escapar de combates
- 💪 Elixir de Força (80 ouro) - +5 Força temporária
- ✨ Elixir de Magia (80 ouro) - +5 Magia temporária

**Armas (específicas por classe):**
- 🗡️ Adagas Gêmeas (300 ouro) - Assassino
- 🏹 Arco Élfico (350 ouro) - Arqueiro
- 🔮 Cajado Arcano (400 ouro) - Mago

**Armaduras:**
- 🛡️ Escudo de Ferro (250 ouro) - Soldado

## Observações

- O token gerado no login é temporário (expira em 30 minutos) e garante que cada usuário só acesse seus próprios dados.
- Mantenha sua chave secreta (`SECRET_KEY`) protegida e nunca compartilhe o arquivo `firebase.json`

## Próximos Passos (Endpoints Backend para Loja)

~~Para que a loja funcione completamente integrada com o backend, os seguintes endpoints precisam ser implementados:~~

### ✅ IMPLEMENTADO! Sistema de Loja Completo

Todos os endpoints foram implementados e estão funcionais:

### 1. ✅ Transações da Loja
```python
# POST /shop/buy
# Compra um item da loja
# Body: { 
#   "character_name": "NomePersonagem",
#   "item_name": "Poção de Cura",
#   "quantity": 1
# }

# POST /shop/sell
# Vende um item do inventário (50% do valor)
# Body: { 
#   "character_name": "NomePersonagem",
#   "item_name": "Poção de Cura",
#   "quantity": 1
# }

# GET /shop/items
# Retorna todos os itens disponíveis na loja

# GET /personagens/{character_name}/gold
# Retorna o ouro atual do personagem
```

### 2. ✅ Validações Implementadas
- Verificação de ouro suficiente antes da compra
- Validação de restrições de classe
- Verificação de item no inventário antes da venda
- Cálculo automático de preço de venda (50% do original)
- Atualização automática do Firebase

### 3. ✅ Persistência no Firebase
- Campo `gold` salvo automaticamente
- Inventário (`itens`) atualizado em tempo real
- Transações atômicas garantidas

**📖 Documentação completa em:** `INTEGRACAO_LOJA_FIREBASE.md`

---

## Como Testar o Sistema de Loja

1. **Inicie o sistema:**
   ```bash
   python run.py
   ```

2. **Crie um personagem novo** (receberá 100 moedas)

3. **Abra a loja** no menu do jogo

4. **Compre um item** (ex: Poção de Cura - 50 ouro)

5. **Feche e reabra a loja** - O ouro estará atualizado! ✅

6. **Venda um item** - Receba 50% do valor de volta

7. **Verifique no Firebase Console** - Dados persistidos! ✅

---

## Estrutura do Banco de Dados (Firebase)

~~### Estrutura Sugerida no Firestore~~

### ✅ Estrutura Implementada e Funcionando
```json
{
  "users": {
    "usuario123": {
      "personagens": {
        "Aragorn": {
          "name": "Aragorn",
          "character_class": "Soldado",
          "level": 1,
          "gold": 1000,
          "itens": {
            "Poção de Cura": 3,
            "Escudo de Ferro": 1
          },
          "status": { ... }
        }
      }
    }
  }
}
```

## Contribuições

Este projeto está em desenvolvimento ativo. Sugestões e melhorias são bem-vindas!

