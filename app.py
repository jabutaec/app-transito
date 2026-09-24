import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página para ficar com visual de App no celular
st.set_page_config(page_title="Rotina Escolar", page_icon="🚌", layout="centered")

st.title("🚌 Decisão de Turno Escolar")
st.markdown("Acompanhamento em tempo real do trânsito (Casa $\\leftrightarrow$ Escola)")

# 1. Conexão com os Dados (Google Sheets publicado na web em formato CSV)
# Substitua pela URL do seu Google Sheets exportado como CSV
@st.cache_data(ttl=300) # Atualiza os dados a cada 5 minutos
def carregar_dados():
    try:
        # Exemplo de URL: "https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/export?format=csv"
        # Para testar agora, criamos dados simulados caso não haja URL:
        df = pd.DataFrame({
            "hora_consulta": ["06:40", "06:45", "06:50", "06:55", "07:00", "07:05", "18:00", "18:05", "18:10", "18:15", "18:20"],
            "turno_alvo": ["MANHA", "MANHA", "MANHA", "MANHA", "MANHA", "MANHA", "TARDE", "TARDE", "TARDE", "TARDE", "TARDE"],
            "sentido": ["CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "ESCOLA_CASA", "ESCOLA_CASA", "ESCOLA_CASA", "ESCOLA_CASA", "ESCOLA_CASA"],
            "tempo_com_transito_min": [25, 28, 35, 42, 50, 48, 30, 35, 45, 55, 60]
        })
        return df
    except Exception as e:
        st.error("Erro ao carregar dados.")
        return pd.DataFrame()

df = carregar_dados()

if not df.empty:
    # Filtros na tela
    turno_selecionado = st.radio("Selecione o Turno para Análise:", ["MANHA", "TARDE"], horizontal=True)
    
    # Filtrar dados com base na seleção
    df_filtrado = df[df["turno_alvo"] == turno_selecionado]
    
    if not df_filtrado.empty:
        # Métricas de Resumo
        tempo_medio = round(df_filtrado["tempo_com_transito_min"].mean(), 1)
        tempo_pior = df_filtrado["tempo_com_transito_min"].max()
        
        col1, col2 = st.columns(2)
        col1.metric("Tempo Médio no Trânsito", f"{tempo_medio} min")
        col2.metric("Pior Cenário Registrado", f"{tempo_pior} min", delta="Pico de trânsito", delta_color="inverse")
        
        st.divider()
        
        # Gráfico Interativo
        st.subheader(f"Evolução do Trânsito - Turno da {turno_selecionado.capitalize()}")
        fig = px.line(
            df_filtrado, 
            x="hora_consulta", 
            y="tempo_com_transito_min", 
            markers=True,
            title="Minutos gastos por horário de saída",
            labels={"hora_consulta": "Horário da Consulta", "tempo_com_transito_min": "Tempo (Minutos)"},
            color_discrete_sequence=["#FF4B4B"]
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tabela de dados detalhados (opcional, oculto em um menu sanfona)
        with st.expander("Ver dados brutos"):
            st.dataframe(df_filtrado, use_container_width=True)
    else:
        st.warning("Ainda não há dados coletados para este turno.")