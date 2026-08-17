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

Este repositório contém um dashboard analítico completo construído em Python, desenvolvido para explorar a base histórica de sinistros rodoviários brasileiros entre **2007 e 2025**.

A interface interativa resolve o desafio de ler e filtrar milhões de linhas em hardwares modestos, aplicando técnicas de gerenciamento de memória e cache disponíveis no Streamlit.

### Dados Processados

* Histórico de quase duas décadas de ocorrências.
* Base extraída dos Dados Abertos da PRF.
* Dados agrupados por pessoa.
* **4.863.193 registros** consolidados.

## 🏆 Destaques e Otimizações de Processamento

A arquitetura visual foi desenvolvida para não ser apenas estética, mas também **funcional, performática e eficiente em memória**.

### Volumetria Massiva na RAM

Carga interativa de **4.863.193 registros consolidados**, lidos diretamente de uma *view* do banco de dados.

### Otimização de Memória com `category`

Redução significativa do consumo de memória do Pandas ao transformar colunas de texto com valores repetitivos — como **UFs, fase do dia e estado físico** — em dados categóricos.

### Filtros em Camadas

Implementação de uma lógica de interface dinâmica na qual a seleção de **Macrorregiões do IBGE** refina automaticamente as opções de **UFs** disponíveis para o usuário.

### Tematização Consistente

Utilização de injeção de CSS no BaseWeb do Streamlit e parametrização explícita no Plotly para garantir um **Dark Mode** consistente, limpo e legível.

## 🔍 Análise Exploratória Detalhada — Em Breve

Esta seção será atualizada na **Fase 2 do projeto**, na qual serão aprofundadas as análises estatísticas, os testes de hipóteses e a identificação de correlações relacionadas aos sinistros.

* **Análise Temporal e Sazonalidade:** `Em desenvolvimento`
* **Análise Geoespacial e Rotas Críticas:** `Em desenvolvimento`
* **Correlação de Letalidade vs. Condições (Clima/Pista):** `Em desenvolvimento`

## 🛠️ Stack Utilizada

| Componente               | Ferramenta                       | Propósito                                          |
| ------------------------ | -------------------------------- | -------------------------------------------------- |
| **Interface / Frontend** | Streamlit                        | Criação do dashboard interativo em Python          |
| **Data Visualization**   | Plotly (Express / Graph Objects) | Gráficos e KPIs com renderização de alta qualidade |
| **Data Processing**      | Pandas                           | Filtragem, agregação e tipagem categórica          |
| **Conexão com o DB**     | SQLAlchemy + psycopg2-binary     | Conector e engine de leitura segura via `.env`     |
| **Data Warehouse**       | PostgreSQL                       | Hospedagem da dos dados de sinistros  |

## 📂 Estrutura Parcial do Repositório

```text
prf-data-analysis/
│
├── dashboard_visao_geral.py    # Script principal do Dashboard(Streamlit)
├── .env.example                # Template de variáveis de conexão ao BD
├── requirements.txt            # Dependências Python
└── README.md                   # Documentação atual
```

## 🚀 Como Usar — Ambiente Local

### 1. Pré-requisitos e Setup do Ambiente

A análise consome dados vindos diretamente do Data Warehouse relacional criado em ![data-pipeline-prf-sinistrostransito](https://github.com/raphaelcortesdev/data-pipeline-prf-sinistrostransito). Portanto, é necessário primeiramente rodar o pipeline para executar a análise.
> Não é necessário o uso do conteiner para rodar o pipeline.

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
