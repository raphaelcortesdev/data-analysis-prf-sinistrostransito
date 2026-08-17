## 📊 Visão Geral

Este repositório contém um dashboard analítico completo construído em Python, desenvolvido para explorar a base histórica de sinistros rodoviários brasileiros entre **2007 e 2025**.

A interface interativa resolve o desafio de ler e filtrar milhões de linhas em hardwares modestos, aplicando técnicas de gerenciamento de memória e cache disponíveis no Streamlit.

![visao_geral.gif](../assets/visao_geral.gif)

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
