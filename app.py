import streamlit as st
import pandas as pd
from datetime import datetime
import iot_simulation
import analysis
import reports
import streamlit as st

# CSS para menu superior com abas e ícone
st.markdown("""
    <style>
    .top-menu {
        width: 100vw;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #ede3d6;
        padding: 0.7rem 2rem 0.7rem 1.5rem;
        border-bottom: 2px solid #a97c50;
        font-family: 'Segoe UI', Arial, sans-serif;
        margin-bottom: 25px;
    }
    .menu-tabs {
        display: flex;
        gap: 2rem;
    }
    .menu-tabs a {
        color: #6e4b2a;
        font-weight: 600;
        text-decoration: none;
        font-size: 1.12rem;
        padding-bottom: 2px;
        border-bottom: 2px solid transparent;
        transition: border-bottom .2s;
    }
    .menu-tabs a.selected {
        border-bottom: 2px solid #a0522d;
        color: #a0522d;
    }
    .user-icon {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #5b4740;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .user-icon svg {
        fill: #fff;
        width: 24px;
        height: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Controle de aba atual
tab = st.session_state.get("top_menu_tab", "Reservas")
selected_tab = st.experimental_get_query_params().get("tab", [tab])[0]
def change_tab(tab_name):
    st.experimental_set_query_params(tab=tab_name)

# Renderiza o menu HTML
st.markdown(f"""
    <div class="top-menu">
        <div class="menu-tabs">
            <a href="#" {'class="selected"' if selected_tab=='Reservas' else ''} onclick="window.location.search='?tab=Reservas'">Reservas</a>
            <a href="#" {'class="selected"' if selected_tab=='Reservar' else ''} onclick="window.location.search='?tab=Reservar'">Reservar</a>
        </div>
        <div class="user-icon">
            <!-- Ícone SVG -->
            <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="5"/><path d="M12 14c-5 0-9 2-9 5v1h18v-1c0-3-4-5-9-5z"/></svg>
        </div>
    </div>
""", unsafe_allow_html=True)

# Exemplo de conteúdo de cada aba (adicione os seus conteúdos reais nesses blocos)
if selected_tab == "Reservas":
    st.write("Conteúdo de Reservas aqui.")
elif selected_tab == "Reservar":
    st.write("Conteúdo de Reservar aqui.")
else:
    st.write("Selecione uma aba no menu.")


st.set_page_config(page_title="Smart Office 4.0", layout="wide")

st.title("Smart Office 4.0 - Plataforma de Gerenciamento e Monitoramento")

menu = ["Dashboard Projeto", "Monitoramento IoT", "Análise e Insights", "Relatórios IA"]
choice = st.sidebar.selectbox("Navegação", menu)

@st.cache_data
def carregar_backlog():
    return pd.read_csv("data/backlog.csv")

if choice == "Dashboard Projeto":
    st.header("Dashboard de Gerenciamento de Projeto")
    backlog = carregar_backlog()
    st.subheader("Product Backlog")
    st.dataframe(backlog)

    sprints = list(range(1, 6))
    pontos_restantes = [50, 40, 30, 15, 0]
    st.line_chart(pd.DataFrame({"Sprint": sprints, "Pontos Restantes": pontos_restantes}).set_index("Sprint"))

    velocity = backlog["story_points"].sum() / len(sprints)
    st.metric("Velocity Média", f"{velocity:.2f} pontos/sprint")

    st.subheader("Riscos")
    riscos = pd.DataFrame([
        {"Descrição": "Atraso na entrega do módulo IoT", "Impacto": "Alto"},
        {"Descrição": "Falha na API da IA", "Impacto": "Médio"},
    ])
    st.table(riscos)

elif choice == "Monitoramento IoT":
    st.header("Monitoramento em Tempo Real dos Sensores IoT")
    dados_iot = iot_simulation.gerar_dados_iot()
    st.write("Dados do sensor (última leitura):")
    st.json(dados_iot)

    historico = iot_simulation.carregar_historico()
    st.line_chart(historico[["temperatura", "energia"]])

elif choice == "Análise e Insights":
    st.header("Análise e Insights Estratégicos")
    df_iot = iot_simulation.carregar_historico()
    backlog = carregar_backlog()
    texto_insight = analysis.criar_insights(df_iot, backlog)
    st.write(texto_insight)

elif choice == "Relatórios IA":
    st.header("Geração de Relatórios Inteligentes")

    if st.button("Gerar Relatório de Status"):
        backlog = carregar_backlog()
        kpis = {"velocity": backlog["story_points"].sum() / 5, "pontos_total": backlog["story_points"].sum()}
        resumo = reports.gerar_relatorio_status(kpis)
        st.write(resumo)

    if st.button("Gerar Lições Aprendidas"):
        texto = reports.gerar_licoes_aprendidas()
        st.write(texto)
