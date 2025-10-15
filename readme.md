# ⚔️ Oráculo de Combate de RPG

**Um projeto de Machine Learning para prever a dificuldade de encontros de combate em RPGs de mesa.**

Este projeto demonstra um ciclo completo de desenvolvimento de ML, desde a criação de dados sintéticos e treinamento de modelo até a implantação como um serviço de API full-stack.

---

### ✨ Visão Geral

O balanceamento de combate em sistemas como Dungeons & Dragons é um desafio notório para Mestres de Jogo. As diretrizes existentes são muitas vezes imprecisas, levando a combates frustrantes. O Oráculo de Combate resolve este problema usando um modelo de Machine Learning treinado para analisar as estatísticas de um encontro e prever sua dificuldade real com alta precisão.

### 🚀 Demonstração Ao Vivo (Live Demo)


<p align="center">
  <img src="URL_PARA_GIF_AQUI.gif" alt="Demonstração do Oráculo de Combate que ainda não tem." width="80%">
</p>


---

### 🛠️ Stack de Tecnologia

Este projeto foi construído utilizando as seguintes tecnologias:

*   **Backend:** Python, FastAPI, Uvicorn
*   **Machine Learning & Dados:** XGBoost, Scikit-learn, Pandas, Joblib
*   **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
*   **Infraestrutura & Ferramentas:** Ambientes Virtuais (`venv`), Git

---

### ✅ Principais Funcionalidades

*   **Previsão de Dificuldade:** Classifica os encontros em categorias como Trivial, Fácil, Médio, Difícil ou Mortal.
*   **Cálculo de Probabilidade:** Fornece a probabilidade percentual de vitória para o grupo dos jogadores.
*   **Interface Intuitiva:** Um formulário web simples para inserir os dados do combate sem necessidade de conhecimento técnico.
*   **Modelo Customizado:** O modelo de previsão não é pré-pronto; ele foi treinado do zero a partir de dezenas de milhares de combates simulados.
*   **Arquitetura Desacoplada:** Um frontend independente que consome uma API de backend, uma prática padrão da indústria.

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

**2. Configure o Backend**
```bash
# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate # No Windows: .\venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor da API
uvicorn src.api.main:app --reload
```
O servidor estará rodando em `http://1227.0.0.1:8000`.

**3. Inicie o Frontend**
*   Navegue até a pasta `frontend` no seu explorador de arquivos.
*   Abra o arquivo `index.html` no seu navegador.

A aplicação estará totalmente funcional!

---

### 📈 Possíveis Melhorias Futuras

*   **Contas de Usuário:** Permitir que Mestres salvem seus grupos de jogadores e encontros de combate.
*   **Ciclo de Feedback:** Implementar um sistema onde o Mestre possa informar o resultado real do combate para coletar novos dados e retreinar o modelo periodicamente.
*   **Detalhes Avançados:** Adicionar campos para magias, habilidades especiais e condições do terreno para uma simulação mais rica.

---

### 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.