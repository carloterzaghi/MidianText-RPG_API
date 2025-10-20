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
│   │       ├── character_creation_model.py
│   │       ├── character_model.py
│   │       ├── items_table.py
│   │       ├── user_model.py
│   │       └── classes/
│   │           ├── _main_classes.py
│   │           ├── assassino_class.py
│   │           ├── arqueiro_class.py
│   │           ├── mage_class.py
│   │           └── soldado_class.py
│   │   └── routes/
│   │       ├── login.py
│   │       └── personagens.py
│
├── Frontend/
│   ├── main.py
│   ├── api_client.py
│   ├── character_creator.py
│   └── shop.py
│
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

