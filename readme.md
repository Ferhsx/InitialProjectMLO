# ⚔️ Oráculo de Combate de RPG (v2.0)

**Um projeto de Machine Learning full-stack que utiliza engenharia de features para prever a dificuldade de encontros de combate em RPGs de mesa.**

Este projeto demonstra um ciclo de vida completo de MLOps, desde a simulação de dados calibrados e treinamento de modelo com features derivadas, até a implantação como um serviço de API robusto consumido por uma interface web interativa.

<p align="center">
  <img src="URL_GIF_AQUI.gif" alt="Demonstração do Oráculo de Combate" width="80%">
</p>

---

### ✨ Visão Geral

O balanceamento de combate em sistemas como D&D 5e é um desafio notório para Mestres de Jogo. O Oráculo de Combate resolve este problema usando um modelo XGBoost que vai além das estatísticas básicas. Através da **engenharia de features**, o modelo aprende com as *relações* entre os combatentes (como a diferença de poder, a vantagem numérica e a proporção de HP), resultando em predições de dificuldade notavelmente precisas e intuitivas.

---

### 🛠️ Stack de Tecnologia

*   **Backend & API:** Python, FastAPI, Uvicorn
*   **Machine Learning & Dados:** XGBoost, Scikit-learn, Pandas, Joblib
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
*   **Ferramentas de Desenvolvimento:** Ambientes Virtuais (`venv`), Git, Argparse, Dataclasses

---

### ✅ Principais Funcionalidades

*   **Engenharia de Features Avançada:** O coração do projeto. O modelo não usa apenas dados brutos, mas aprende com features criadas para capturar a dinâmica do combate, como:
    *   `hp_ratio`: A proporção de vitalidade entre jogadores e monstros.
    *   `damage_diff`: A diferença no poder de fogo total por rodada.
    *   `level_diff`: A disparidade de nível entre os dois grupos.
    *   E muitas outras...
*   **Simulação de Dados Calibrada:** O dataset foi gerado por um simulador customizado que cria encontros balanceados e variados, evitando o viés de dificuldade e garantindo que o modelo aprenda com uma ampla gama de cenários.
*   **Previsão de Dificuldade e Probabilidade:** Classifica os encontros (Trivial, Fácil, Médio, Difícil, Mortal) e fornece a probabilidade de vitória dos jogadores.
*   **Arquitetura Robusta:**
    *   **Consistência Treino/Inferência:** A mesma lógica de engenharia de features é aplicada tanto no treinamento (`train.py`) quanto na API (`main.py`), evitando o *training-serving skew*.
    *   **Metadados do Modelo:** O modelo é salvo junto com metadados cruciais (como a ordem das features), tornando a implantação mais segura e confiável.
*   **Interface de Usuário Interativa:** Um frontend simples e eficiente para que qualquer usuário possa acessar o poder do modelo sem precisar de conhecimento técnico.

---

### ⚙️ Como Executar Localmente

Siga os passos abaixo para executar o projeto na sua própria máquina.

**Pré-requisitos:**
*   Python 3.10+
*   Git

**1. Clone o Repositório**
```bash
git clone https://github.com/seu-usuario/InitialProjectMLO.git
cd InitialProjectMLO
```

**2. Configure o Ambiente**
```bash
# Crie e ative um ambiente virtual
python -m venv venv
# No Windows (PowerShell): .\venv\Scripts\activate
# No Linux/macOS: source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

**3. Geração de Dados e Treinamento (Se necessário)**
O repositório já inclui um modelo pré-treinado. Se quiser refazer o processo:
```bash
# Gere um novo dataset (pode levar alguns minutos)
python src/data_creation/simulador.py --n 100000

# Treine um novo modelo com o dataset gerado
python src/model_training/train.py
```

**4. Inicie o Servidor da API**
```bash
uvicorn src.api.main:app --reload
```
O servidor estará rodando em `http://127.0.0.1:8000`. Você pode testar os endpoints na documentação interativa em `http://127.0.0.1:8000/docs`.

**5. Inicie o Frontend**
*   Navegue até a pasta `frontend` no seu explorador de arquivos.
*   Abra o arquivo `index.html` no seu navegador.

A aplicação estará totalmente funcional e pronta para uso!