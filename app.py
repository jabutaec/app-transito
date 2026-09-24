import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Rotina Escolar", page_icon="🚌", layout="centered")

st.title("🚌 Decisão de Turno Escolar")
st.markdown("Acompanhamento do tempo de trajeto simulado")

# Gerando dados de teste diretamente para garantir que a tela carregue
def carregar_dados_teste():
    df = pd.DataFrame({
        "hora_consulta": ["06:40", "06:45", "06:50", "06:55", "07:00", "07:05", "18:00", "18:05", "18:10", "18:15", "18:20"],
        "turno_alvo": ["MANHA", "MANHA", "MANHA", "MANHA", "MANHA", "MANHA", "TARDE", "TARDE", "TARDE", "TARDE", "TARDE"],
        "sentido": ["CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "CASA_ESCOLA", "ESCOLA_CASA", "ESCOLA_CASA", "ESCOLA_CASA", "ESCOLA_CASA", "ESCOLA_CASA"],
        "tempo_com_transito_min": [25, 28, 35, 42, 50, 48, 30, 35, 45, 55, 60]
    })
    return df

# Forçando o uso dos dados de teste
df = carregar_dados_teste()

if not df.empty:
    # Seleção de turno
    turno_selecionado = st.radio("Selecione o Turno para Análise:", ["MANHA", "TARDE"], horizontal=True)
    
    # Filtro
    df_filtrado = df[df["turno_alvo"] == turno_selecionado]
    
    if not df_filtrado.empty:
        # Métricas
        tempo_medio = round(df_filtrado["tempo_com_transito_min"].mean(), 1)
        tempo_pior = df_filtrado["tempo_com_transito_min"].max()
        
        col1, col2 = st.columns(2)
        col1.metric("Tempo Médio", f"{tempo_medio} min")
        col2.metric("Pior Cenário", f"{tempo_pior} min")
        
        st.divider()
        
        # Gráfico
        st.subheader(f"Evolução do Trânsito - Turno: {turno_selecionado}")
        fig = px.line(
            df_filtrado, 
            x="hora_consulta", 
            y="tempo_com_transito_min", 
            markers=True,
            title="Minutos gastos por horário",
            color_discrete_sequence=["#FF4B4B"]
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Sem dados para o turno selecionado.")
else:
    st.error("Falha ao carregar a estrutura de dados.")
