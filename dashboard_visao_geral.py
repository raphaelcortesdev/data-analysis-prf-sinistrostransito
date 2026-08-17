import os
import urllib.parse
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
import streamlit as st

# ==========================================
# 0. CONFIGURAÇÃO DA PÁGINA E CSS CUSTOMIZADO
# ==========================================
st.set_page_config(page_title="Dashboard PRF", layout="wide")

st.markdown("""
    <style>
        .stApp {
            background-color: #333333;
        }
        h1, h2, h3, p, span, div {
            color: #F4F6F9;
        }
        .kpi-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
        }
        .kpi-title {
            font-size: 16px;
            color: #1A2B4C;
            font-weight: bold;
        }
        .kpi-value {
            font-size: 28px;
            font-weight: bold;
        }
        .header-bg {
            background-color: #333333;
            padding: 20px;
            border-radius: 5px;
            color: white !important;
            margin-bottom: 20px;
        }
        .header-bg h1 {
            color: white !important;
            margin: 0;
        }
        
        div[data-baseweb="select"] > div {
            background-color: white !important;
            border-radius: 8px !important;
        }
        div[data-baseweb="select"] * {
            color: #333333 !important;
        }
        
        div[data-baseweb="popover"] div {
            background-color: white !important;
            color: #333333 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Mapeamento das Macrorregiões do IBGE
MACRORREGIOES = {
    'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MS', 'MT'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

# ==========================================
# 1. CONEXÃO E EXTRAÇÃO DE DADOS (COM CACHE)
# ==========================================
@st.cache_data(ttl=3600) 
def load_data():
    load_dotenv(find_dotenv(), override=True)
    user = os.getenv('DB_USER')
    db_pass_raw = os.getenv('DB_PASSWORD') or ''
    password = urllib.parse.quote_plus(db_pass_raw) 
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    
    query = """
    SELECT 
        id_acidente_original, 
        ano, 
        uf, 
        fase_dia, 
        br, 
        faixa_etaria, 
        sexo, 
        estado_fisico 
    FROM view_geral
    """
    df = pd.read_sql(query, engine)
    
    df.fillna('Não Informado', inplace=True)
    df['ano'] = df['ano'].astype(int)
    
    # Categoriza colunas de texto para otimizar uso de memória no ato de carregamento
    colunas_texto = ['uf', 'fase_dia', 'br', 'faixa_etaria', 'sexo', 'estado_fisico']
    for col in colunas_texto:
        df[col] = df[col].astype('category')
        
    return df

df_geral = load_data()

# ==========================================
# CABEÇALHO E FILTROS
# ==========================================
st.markdown('<div class="header-bg"><h1>Sinistros de Trânsito Em Rodovias Federais - Visão Geral (2007-2025)</h1></div>', unsafe_allow_html=True)

# 4 filtros em 4 colunas
col_f1, col_f2, col_f3, col_f4 = st.columns(4)

with col_f1:
    anos_disponiveis = sorted(df_geral['ano'].unique().tolist())
    anos_selecionados = st.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

with col_f2:
    regioes_disponiveis = list(MACRORREGIOES.keys())
    regioes_selecionadas = st.multiselect("Região", regioes_disponiveis, default=regioes_disponiveis)

with col_f3:
    # Filtra as UF de acordo com as macrorregiões estabelecidas em MACRORREGIOES{}
    ufs_elegiveis = []
    for reg in regioes_selecionadas:
        ufs_elegiveis.extend(MACRORREGIOES.get(reg, []))
    
    ufs_disponiveis = sorted([uf for uf in df_geral['uf'].unique() if uf in ufs_elegiveis])
    ufs_selecionadas = st.multiselect("UF", ufs_disponiveis, default=ufs_disponiveis)

with col_f4:
    fases_disponiveis = sorted(df_geral['fase_dia'].unique().tolist())
    fases_selecionadas = st.multiselect("Fase do Dia", fases_disponiveis, default=fases_disponiveis)

df_filtrado = df_geral[
    (df_geral['ano'].isin(anos_selecionados)) &
    (df_geral['uf'].isin(ufs_selecionadas)) &
    (df_geral['fase_dia'].isin(fases_selecionadas))
]

# ==========================================
# BLOCO 2: CARTÕES DE KPI
# ==========================================
col_k1, col_k2, col_k3, col_k4 = st.columns(4)

total_sinistros = df_filtrado['id_acidente_original'].nunique()
pessoas_envolvidas = len(df_filtrado)
vitimas_fatais = len(df_filtrado[df_filtrado['estado_fisico'] == 'obito'])
taxa_letalidade = (vitimas_fatais / pessoas_envolvidas * 100) if pessoas_envolvidas > 0 else 0

def kpi_card(title, value, color="#2980B9"):
    return f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value" style="color: {color};">{value}</div>
        </div>
    """

col_k1.markdown(kpi_card("Total de Sinistros", f"{total_sinistros:,.0f}".replace(',', '.')), unsafe_allow_html=True)
col_k2.markdown(kpi_card("Pessoas Envolvidas", f"{pessoas_envolvidas:,.0f}".replace(',', '.')), unsafe_allow_html=True)
col_k3.markdown(kpi_card("Vítimas Fatais", f"{vitimas_fatais:,.0f}".replace(',', '.'), color="#C0392B"), unsafe_allow_html=True)
col_k4.markdown(kpi_card("Taxa de Letalidade", f"{taxa_letalidade:.2f}%".replace('.', ','), color="#C0392B"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# BLOCO 3: VISÃO GERAL
# ==========================================
col_b3_1, col_b3_2 = st.columns([6, 4])

with col_b3_1:
    st.subheader("Variação de Sinistros e Óbitos ao longo do tempo")
    df_tendencia = df_filtrado.groupby('ano').agg(
        total_sinistros=('id_acidente_original', 'nunique'),
        vitimas_fatais=('estado_fisico', lambda x: (x == 'obito').sum())
    ).reset_index()
    
    fig_linha = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig_linha.add_trace(go.Scatter(x=df_tendencia['ano'], y=df_tendencia['total_sinistros'], name="Sinistros", line=dict(color='#2980B9', width=3)), secondary_y=False)
    fig_linha.add_trace(go.Scatter(x=df_tendencia['ano'], y=df_tendencia['vitimas_fatais'], name="Óbitos", line=dict(color='#C0392B', width=3)), secondary_y=True)

    fig_linha.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#333333'),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    fig_linha.update_xaxes(showgrid=True, gridcolor='#E5E8EC', tickfont=dict(color='#333333'))
    fig_linha.update_yaxes(title_text="Total de Sinistros", secondary_y=False, showgrid=True, gridcolor='#E5E8EC', title_font=dict(color='#333333'), tickfont=dict(color='#333333'))
    fig_linha.update_yaxes(title_text="Vítimas Fatais", secondary_y=True, showgrid=False, title_font=dict(color='#333333'), tickfont=dict(color='#333333'))
    
    st.plotly_chart(fig_linha, use_container_width=True)

with col_b3_2:
    st.subheader("Top 10 Rodovias (BR)")
    df_br = df_filtrado[df_filtrado['br'] != 'Não Informado']
    df_br_agrupado = df_br.groupby('br')['id_acidente_original'].nunique().reset_index()
    df_br_agrupado = df_br_agrupado.sort_values(by='id_acidente_original', ascending=False).head(10)
    
    df_br_agrupado['br'] = "BR-" + df_br_agrupado['br'].astype(str)
    
    fig_bar = px.bar(df_br_agrupado, x='id_acidente_original', y='br', orientation='h', color_discrete_sequence=['#5DADE2'])
    fig_bar.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#333333'),
        yaxis={'categoryorder':'total ascending'}, 
        xaxis_title="Total de Sinistros", 
        yaxis_title=""
    )
    fig_bar.update_xaxes(showgrid=True, gridcolor='#E5E8EC', tickfont=dict(color='#333333'), title_font=dict(color='#333333'))
    fig_bar.update_yaxes(tickfont=dict(color='#333333'))
    
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("<hr/>", unsafe_allow_html=True)

# ==========================================
# BLOCO 4: PERFIL (RODAPÉ)
# ==========================================
col_b4_1, col_b4_2, col_b4_3 = st.columns(3)

with col_b4_1:
    st.subheader("Sinistros por UF")
    df_uf = df_filtrado[df_filtrado['uf'] != 'Não Informado'].groupby('uf')['id_acidente_original'].nunique().reset_index()
    
    fig_tree = px.treemap(
        df_uf, 
        path=['uf'], 
        values='id_acidente_original', 
        color='id_acidente_original', 
        color_continuous_scale='Blues'
    )
    
    fig_tree.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#333333'),
        margin=dict(t=10, l=10, r=10, b=10),
        coloraxis_colorbar=dict(
            tickfont=dict(color='#333333'),
            title=dict(font=dict(color='#333333'))
        )
    )
    st.plotly_chart(fig_tree, use_container_width=True)

with col_b4_2:
    st.subheader("Estado Físico do Envolvido")
    df_estado = df_filtrado[df_filtrado['estado_fisico'] != 'Não Informado']['estado_fisico'].value_counts().reset_index()
    df_estado.columns = ['estado_fisico', 'contagem']
    
    cores_estado = {'ileso': '#27AE60', 'lesoes leves': '#F1C40F', 'lesoes graves': '#F39C12', 'obito': '#C0392B'}
    
    fig_donut = px.pie(
        df_estado, 
        values='contagem', 
        names='estado_fisico', 
        hole=0.5, 
        color='estado_fisico', 
        color_discrete_map=cores_estado
    )
    
    fig_donut.update_traces(
        textfont=dict(color='#333333'),
        insidetextfont=dict(color='white')
    )
    
    fig_donut.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#333333'),
        legend=dict(
            orientation="h", 
            yanchor="bottom", 
            y=-0.2, 
            xanchor="center", 
            x=0.5,
            font=dict(color='#333333')
        )
    )
    st.plotly_chart(fig_donut, use_container_width=True)
with col_b4_3:
    st.subheader("Sexo e Faixa Etária")
    df_sexo_idade = df_filtrado[(df_filtrado['faixa_etaria'] != 'Não Informado') & (df_filtrado['sexo'].isin(['masculino', 'feminino']))]
    df_sexo_idade = df_sexo_idade.groupby(['faixa_etaria', 'sexo']).size().reset_index(name='contagem')
    
    fig_colunas = px.bar(df_sexo_idade, x='faixa_etaria', y='contagem', color='sexo', barmode='stack', color_discrete_map={'masculino': '#1A2B4C', 'feminino': '#5DADE2'})
    fig_colunas.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(color='#333333'),
        xaxis_title="", 
        yaxis_title="Quantidade de Pessoas", 
        legend=dict(title="")
    )
    fig_colunas.update_xaxes(tickfont=dict(color='#333333'))
    fig_colunas.update_yaxes(showgrid=True, gridcolor='#E5E8EC', tickfont=dict(color='#333333'), title_font=dict(color='#333333'))
    st.plotly_chart(fig_colunas, use_container_width=True)