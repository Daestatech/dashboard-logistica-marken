# 🚚 Central Logística Inteligente – Gestão de Transferência entre Lojas

Este projeto tem como objetivo otimizar a gestão de estoque entre lojas da rede, identificando automaticamente excessos, rupturas e sugerindo transferências inteligentes entre unidades.

A solução foi desenvolvida em Python utilizando Streamlit, permitindo uma visualização simples, rápida e prática para tomada de decisão operacional.

---

# 🎯 Objetivo

Reduzir:

* 📦 Estoque parado
* 💸 Compras desnecessárias
* 🏪 Ruptura de produtos nas lojas

E melhorar:

* 🔄 Giro de estoque
* 📊 Distribuição entre lojas
* 🚚 Logística interna

---

# ⚙️ Funcionalidades

## 🔍 Análise automática de estoque por loja

* Identifica produtos com excesso e falta
* Detecta desequilíbrio entre unidades

## 🚨 Sugestão inteligente de transferências

* Transferência URGENTE (loja com estoque zero)
* Redistribuição (diferença elevada)
* Status equilibrado

## 📊 Dashboard interativo

* KPIs logísticos
* Ranking de produtos críticos
* Visualização clara por produto

## ❌ Filtro automático de produtos

Ignora itens que não fazem sentido transferir:

* FLV (Frutas, Legumes e Verduras)
* BOVINO
* SUINO

---

# 📂 Estrutura do Projeto

```bash
dashboard_logistica_inteligente.py
requirements.txt
README.md
```

---

# 📥 Entrada de dados

O sistema utiliza um relatório exportado do ERP com estrutura semelhante a:

* DESCCOMPLETA (descrição do produto)
* EMPRESA_X (nome da loja)
* ESTOQUE_X (quantidade em estoque)

Exemplo:

| Produto   | Loja A     | Estoque | Loja B    | Estoque |
| --------- | ---------- | ------- | --------- | ------- |
| Produto X | 01-CENTRAL | 50      | 02-LOJA B | 0       |

---

# 🚀 Como executar o projeto

## 1. Instalar dependências

```bash
pip install -r requirements.txt
```

## 2. Executar o dashboard

```bash
streamlit run dashboard_logistica_inteligente.py
```

## 3. Abrir no navegador

O sistema abrirá automaticamente em:

```
http://localhost:8501
```

---

# 🧠 Lógica de decisão

Para cada produto:

* Identifica loja com maior estoque (origem)
* Identifica loja com menor estoque (destino)
* Calcula o desequilíbrio

### Classificação:

| Situação              | Ação                     |
| --------------------- | ------------------------ |
| Estoque 0 em uma loja | 🚨 Transferência urgente |
| Diferença alta        | 🔄 Redistribuição        |
| Equilíbrio            | ✅ Nenhuma ação           |

---

# 📊 KPIs disponíveis

* Quantidade de produtos analisados
* Total de desequilíbrio da rede
* Número de transferências urgentes

---

# 💡 Benefícios do uso

* Redução imediata de compras desnecessárias
* Melhor aproveitamento do estoque existente
* Aumento da disponibilidade de produtos nas lojas
* Melhoria no fluxo de caixa

---

# 🔮 Próximas evoluções

* 💰 Cálculo financeiro das transferências
* 📦 Cobertura de estoque por loja (dias)
* 🚚 Roteirização de transferências
* 🤖 Sugestão automática de compras
* 🔐 Controle de acesso por usuário

---

# 🛠️ Tecnologias utilizadas

* Python
* Streamlit
* Pandas
* OpenPyXL

---

# 👨‍💻 Autor

Projeto desenvolvido por Altamiro - Daesta Tech.

---

# 📌 Observações

Este projeto faz parte de uma iniciativa de transformação digital focada em:

* automação de processos
* inteligência operacional
* tomada de decisão baseada em dados

---

# 🚀 Status do Projeto

✅ Em uso
🔄 Em evolução contínua

---
