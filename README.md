# 🤖 **Projeto CHAMA — Módulo de Machine Learning (CBMPE)**  

> 💡 *Módulo de Machine Learning desenvolvido para prever a demanda de ocorrências do Corpo de Bombeiros Militar de Pernambuco (CBMPE), utilizando dados históricos reais e integrado ao sistema CHAMA.*

---

## 🌐 **Deploy / Integração**

**Modelo consumido via API:**  
🔗 Integrado ao backend do sistema CHAMA (Node.js + Express)

**Backend (API):**  
🧩 https://backend-chama.up.railway.app/


---

## 🧭 **Visão Geral**

Este repositório contém o **módulo de Machine Learning do sistema CHAMA**, responsável por prever a demanda futura de ocorrências com base em dados históricos reais do CBMPE.

O modelo foi desenvolvido após todo o processo de **tratamento, padronização, modelagem e migração dos dados**, que originalmente estavam dispersos em planilhas Excel e passaram a ser armazenados em um banco relacional MySQL.

🎯 **Objetivo do modelo:**  
Apoiar o planejamento operacional do CBMPE, fornecendo previsões que auxiliam na alocação de equipes, viaturas e recursos.

---

## 📊 **Dados**

- 📌 Origem: registros históricos reais de ocorrências do CBMPE  
- 🧹 Tratamento: limpeza, padronização e validação manual  
- 🗄️ Armazenamento: MySQL  
- 🔄 Migração: planilhas Excel → banco relacional via TypeORM  
- 🧠 Features utilizadas:
  - Município  
  - Dia da semana  
  - Histórico de volume de ocorrências  

---

## 🧠 **Modelo de Machine Learning**

- Algoritmo: **XGBoost Regressor**
- Tipo: Regressão supervisionada
- Objetivo: prever o número de ocorrências por município e dia da semana
- Split dos dados: aproximadamente **80% treino / 20% teste**

---

## 📈 **Avaliação do Modelo**

- **R² ≈ 0,80**  
  → O modelo explica cerca de 80% da variabilidade dos dados históricos.

- **MAE ≈ 1,6 ocorrências/dia**  
  → Em média, a previsão diária apresenta um erro de aproximadamente 1 a 2 ocorrências.

🔎 **Observação importante:**  
A previsão diária é naturalmente mais volátil. Em análises agregadas (semanais ou mensais), o erro relativo diminui significativamente, tornando o modelo mais estável e confiável para apoio à tomada de decisão estratégica.

---

## 🔌 **Integração com o Sistema**

O modelo:
- roda como uma **API**
- é integrado ao **backend** do CHAMA
- é consumido diretamente pelo **frontend**
- alimenta dashboards preditivos em tempo real

---

## 🧰 **Stack Tecnológica**

| Camada | Tecnologias |
|------|-------------|
| **Linguagem** | Python |
| **Modelagem** | XGBoost |
| **Manipulação de Dados** | Pandas, NumPy |
| **API** | FastAPI / Flask |
| **Banco de Dados** | MySQL |
| **Integração** | Node.js + Express |

---

## 🧪 **Como rodar localmente**

1️⃣ **Clone o repositório**
```bash

2️⃣ **Instale as dependências**

pip install -r requirements.txt

3️⃣ **Execute a API**

uvicorn main:app --reload


📌 Contexto do Projeto CHAMA

O módulo de ML faz parte do sistema CHAMA, desenvolvido no terceiro semestre da faculdade para o Corpo de Bombeiros Militar de Pernambuco (CBMPE), com foco em:

padronização dos registros de ocorrência

redução de retrabalho

integração entre sistemas

geração de dashboards operacionais e preditivos

📜 Licença

Projeto acadêmico desenvolvido no SENAC Pernambuco. Consulte o arquivo LICENSE (se disponível) para mais informações.
