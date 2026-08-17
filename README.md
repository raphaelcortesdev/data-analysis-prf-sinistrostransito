![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.1.4+-150458?logo=pandas&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/raphael-cortes-b0b544305/)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/raphaelcorte_s/)
[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=flat&logo=whatsapp&logoColor=white)](https://wa.me/5561998294492)

# PRF Data Analysis — Dashboard e Visão Geral

Projeto focado na **visualização e análise de dados de sinistros de trânsito da PRF (Polícia Rodoviária Federal)**.
> Ainda em desenvolvimento

## 📊 Visão Geral

![visao_geral.gif](./assets/visao_geral.gif)
**Dashboard interativo com uma visão geral dos dados entre 2007 e 2025.**

### Destaques

- 4.863.193 registros consolidados
- Otimização de memória
- Filtros em Camadas (macrorregiões e UF)

Veja mais em ![**VISAO GERAL**](/visao_geral/)

## 🔍 Análise Exploratória Detalhada

> Em desenvolvimento

## 🛠️ Stack Utilizada

| Componente               | Ferramenta                       | Propósito                                          |
| ------------------------ | -------------------------------- | -------------------------------------------------- |
| **Interface / Frontend** | Streamlit                        | Criação do dashboard interativo em Python          |
| **Data Visualization**   | Plotly (Express / Graph Objects) | Gráficos e KPIs com renderização de alta qualidade |
| **Data Processing**      | Pandas                           | Filtragem, agregação e tipagem categórica          |
| **Conexão com o DB**     | SQLAlchemy + psycopg2-binary     | Conector e engine de leitura segura via `.env`     |
| **Data Warehouse**       | PostgreSQL                       | Hospedagem da dos dados de sinistros  |

## 📂 Estrutura do Repositório

```text
├── analise                            # Analise exploratória (em desenvolvimento)
├── assets                             # Mídias de auxílio
│   └── visao_geral.gif
├── .env.example                       # Exemplo de configuração do .env
├── .gitignore
├── README.md                          # Este arquivo
├── requirements.txt                   # Dependências do projeto
├── visao_geral                        # Visão geral dos dados 
    ├── dashboard_visao_geral.py
    └── README.md


```

## 🚀 Como Usar — Ambiente Local

### 1. Pré-requisitos e Setup do Ambiente

A análise consome dados vindos diretamente do Data Warehouse relacional criado em ![data-pipeline-prf-sinistrostransito](https://github.com/raphaelcortesdev/data-pipeline-prf-sinistrostransito). Portanto, é necessário primeiramente rodar o pipeline para executar a análise.
> Não é necessário o uso do conteiner para rodar o pipeline e/ou a análise.

Recomenda-se fortemente o uso do **Conda** para isolar as bibliotecas e garantir maior compatibilidade entre as dependências.

Crie o ambiente virtual utilizando Python 3.11 ou 3.12:

```bash
conda create --name prf-dashboard python=3.12
conda activate prf-dashboard
```

Em seguida, instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Configurando o Banco de Dados

Crie o arquivo de variáveis `.env` de ambiente na raiz do projeto

Abra o arquivo `.env` e preencha as credenciais de acesso ao PostgreSQL.

> **Importante:** As instruções de como preencher o arquivo .env estão em .env.example

### 3. Executando o Dashboard

Com o ambiente ativado e o arquivo `.env` configurado, execute:

```bash
streamlit run dashboard_visao_geral.py
```

O navegador deverá abrir automaticamente em:

```text
http://localhost:8501
```

Na primeira execução, o carregamento e o processo de cache da base histórica (`Running load_data()`) poderão levar aproximadamente **1 a 2 minutos**.

Após o carregamento inicial, as navegações e filtragens subsequentes serão realizadas de forma significativamente mais rápida devido ao mecanismo de cache utilizado pelo Streamlit.
