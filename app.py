import streamlit as st
import pandas as pd
from datetime import datetime
import iot_simulation
import analysis
import reports
import textwrap

COLOR_MAIN = "#86D9D1"
COLOR_DARK = "#00897B"
COLOR_MID = "#60C5B5"
COLOR_LIGHT = "#00897B"
COLOR_ACCENT = "#43A89E"

st.set_page_config(page_title="Smart Office 4.0", layout="wide")

st.markdown(f"""
    <style>
        body, .reportview-container, .main {{
            background: {COLOR_MAIN} !important;
        }}
        .top-menu {{
            width: 100vw;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: {COLOR_DARK};
            padding: 0.7rem 2rem 0.7rem 1.5rem;
            border-bottom: 2px solid #a97c50;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin-bottom: 25px;
        }}
        .user-icon {{
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background: {COLOR_LIGHT};
            display: flex;
            align-items: center;
            justify-content: center;
            margin-left: 18px;
        }}
        .user-icon svg {{
            fill: #fff;
            width: 24px;
            height: 24px;
        }}
        .stButton>button {{
            background-color: {COLOR_DARK} !important;
            color: #fff !important;
            font-weight: bold !important;
            border-radius: 6px !important;
            border: none !important;
            transition: background 0.2s;
        }}
        .stButton>button:hover {{
            background-color: {COLOR_ACCENT} !important;
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown(f"""
    <div class="top-menu">
        <div style="flex:1 1 auto"></div>
        <div class="user-icon" title="Perfil do Usuário">
            <svg viewBox="0 0 24 24"><circle cx="12" cy="8" r="5"/><path d="M12 14c-5 0-9 2-9 5v1h18v-1c0-3-4-5-9-5z"/></svg>
        </div>
    </div>
""", unsafe_allow_html=True)

# Sidebar: menu principal e login/cadastro
pagina_sistema = st.sidebar.radio("Menu", ["Projeto", "Reservas / Salas"])

with st.sidebar:
    st.markdown("### Perfil do Usuário")
    opcao = st.radio("Ação:", ["Login", "Cadastro"])
    if opcao == "Login":
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            st.success(f"Bem-vindo, {usuario}!")
    else:
        novo_usuario = st.text_input("Novo usuário")
        nova_senha = st.text_input("Nova senha", type="password")
        if st.button("Cadastrar"):
            st.success("Cadastro realizado.")

# ---- ÁREA DE PÁGINA DE RESERVAS/SALAS ----
if pagina_sistema == "Reservas / Salas":
    aba_reservas, aba_reservar = st.tabs(["Reservas", "Reservar"])
    with aba_reservas:
        st.write("Lista de Reservas:")

        reservas = [
            {"nome": "Sophia", "horario": "12:00 até 15:00", "sala": "Copacabana", "data": "22/10/2026"},
            {"nome": "Thalita", "horario": "8:00 até 11:30", "sala": "Niterói", "data": "10/01/2026"},
            {"nome": "Marcos", "horario": "14:00 até 17:30", "sala": "Paulista", "data": "15/03/2026"},
            {"nome": "Emily", "horario": "09:15 até 11:00", "sala": "Barra", "data": "09/05/2026"},
            {"nome": "Luana", "horario": "13:00 até 16:30", "sala": "Ipanema", "data": "20/08/2026"},
            {"nome": "Renato", "horario": "09:00 até 12:00", "sala": "Leblon", "data": "30/12/2026"},
            {"nome": "Camila", "horario": "15:00 até 18:20", "sala": "Botafogo", "data": "02/02/2026"},
            {"nome": "Frankie", "horario": "8:00 até 11:00", "sala": "Savassi", "data": "11/11/2026"},
            {"nome": "Angel", "horario": "10:00 até 13:00", "sala": "Higienópolis", "data": "16/04/2026"},
            {"nome": "Jackson", "horario": "16:00 até 19:00", "sala": "Moema", "data": "28/06/2026"},
        ]
        cols = st.columns(2)
        for idx, r in enumerate(reservas):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="
                    background-color: {COLOR_MAIN};
                    border-radius: 14px;
                    padding: 14px 16px 11px 16px;
                    margin-bottom: 18px;
                    min-width: 220px;
                    max-width: 95%;
                    box-shadow: 0 2px 8px 0 {COLOR_DARK}22;">
                    <h4 style="margin-top: 0; margin-bottom: 10px; color: {COLOR_DARK}; font-size:1.1rem;">Reserva {idx+1}</h4>
                    <p style="font-size:1.03rem; margin-bottom:3px;"><strong>Nome:</strong> {r['nome']}</p>
                    <p style="font-size:1.03rem; margin-bottom:3px;"><strong>Horário:</strong> {r['horario']}</p>
                    <p style="font-size:1.03rem; margin-bottom:3px;"><strong>Sala:</strong> {r['sala']}</p>
                    <p style="font-size:1.03rem; margin-bottom:0;"><strong>Data:</strong> {r['data']}</p>
                </div>
                """, unsafe_allow_html=True)

# ---- ÁREA DO SISTEMA DE PROJETO E DASHBOARD ----
elif pagina_sistema == "Projeto":
    st.title("Smart Office 4.0 - Plataforma de Gerenciamento e Monitoramento")

    menu_proj = [
        "Dashboard Projeto",
        "Monitoramento IoT",
        "Análise e Insights",
        "Relatórios IA",
        "Project Charter",
        "Product Backlog Inicial",
        "Documentação"
    ]
    aba = st.selectbox("", menu_proj)

    @st.cache_data
    def carregar_backlog():
        return pd.read_csv("data/backlog.csv")

    if aba == "Dashboard Projeto":
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

    elif aba == "Monitoramento IoT":
        st.header("Monitoramento em Tempo Real dos Sensores IoT")
        dados_iot = iot_simulation.gerar_dados_iot()
        st.write("Dados do sensor (última leitura):")
        st.json(dados_iot)
        historico = iot_simulation.carregar_historico()
        st.line_chart(historico[["temperatura", "energia"]])

    elif aba == "Análise e Insights":
        st.header("Análise, Insights e Storytelling Estratégico")
        def gerar_insight_estrategico():
            return textwrap.dedent("""\
            Insights Estratégicos Smart Office 4.0

            Após a entrega do módulo 'Sensores de Luz Automáticos' (Sprint 3), foi identificada uma redução de 18% no consumo de energia elétrica dos ambientes monitorados.

            A implementação do recurso 'Controle de Ocupação de Salas' permitiu otimizar a utilização dos espaços, diminuindo em 22% a lotação média por sala nos horários de pico, corroborando a melhoria na gestão de ambientes.

            O dashboard gerencial, integrado ao monitoramento IoT, permitiu decisões em tempo real: por exemplo, ajustes de temperatura realizados conforme padrão de presença, garantindo maior conforto sem desperdício.

            LIÇÕES ESTRATÉGICAS:
            - Integrar dados de IoT ao backlog permite entrega orientada por impacto real.
            - A correlação dos KPIs do projeto e dos sensores potencializa a comunicação com o sponsor.
            - Cada Sprint foi associada a métricas concretas dos sensores, documentando o valor entregue.
            """)

        if st.button("Gerar Insights Estratégicos", key="btn_insight"):
            insight = gerar_insight_estrategico()
            st.markdown(insight)
            st.download_button("Baixar Insights (TXT)", insight, file_name="insights_estrategicos.txt")

            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica", 12)
            y = 750
            c.drawString(50, y, "Insights Estratégicos - Smart Office 4.0")
            y -= 30
            linhas = insight.split("\n")
            for linha in linhas:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, linha[:80])
                y -= 15
            c.save()
            buffer.seek(0)
            st.download_button("Baixar Insights (PDF)", buffer.getvalue(), file_name="insights_estrategicos.pdf", mime="application/pdf")

    elif aba == "Relatórios IA":
        st.header("Geração de Relatórios Inteligentes")
        if st.button("Gerar Relatório de Status", key="relatorio_status"):
            backlog = carregar_backlog()
            kpis = {
                "velocity": backlog["story_points"].sum() / 5,
                "pontos_total": backlog["story_points"].sum()
            }
            resumo = reports.gerar_relatorio_status(kpis)
            st.info("### Relatório de Status Gerado:")
            st.markdown(resumo)
            st.download_button("Baixar Relatório (TXT)", resumo, file_name="relatorio_status.txt")
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica", 12)
            y = 750
            c.drawString(50, y, "Relatório de Status - Smart Office 4.0")
            y -= 30
            linhas = resumo.split("\n")
            for linha in linhas:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, linha[:80])
                y -= 15
            c.save()
            buffer.seek(0)
            st.download_button("Baixar Relatório (PDF)", buffer.getvalue(), file_name="relatorio_status.pdf", mime="application/pdf")

        if st.button("Gerar Lições Aprendidas", key="licoes_aprendidas"):
            texto = reports.gerar_licoes_aprendidas()
            st.info("### Lições Aprendidas Geradas:")
            st.markdown(texto)
            st.download_button("Baixar Lições Aprendidas (TXT)", texto, file_name="licoes_aprendidas.txt")
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica", 12)
            y = 750
            c.drawString(50, y, "Lições Aprendidas - Smart Office 4.0")
            y -= 30
            linhas = texto.split("\n")
            for linha in linhas:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, linha[:80])
                y -= 15
            c.save()
            buffer.seek(0)
            st.download_button("Baixar Lições Aprendidas (PDF)", buffer.getvalue(), file_name="licoes_aprendidas.pdf", mime="application/pdf")

    elif aba == "Project Charter":
        st.header("Project Charter do Projeto")
        def gerar_project_charter():
            return textwrap.dedent("""\
            Project Charter – Smart Office 4.0

            Objetivo:
            Desenvolver uma plataforma integrada para gerenciamento e monitoramento inteligente do escritório, utilizando dados de IoT, dashboards, IA generativa e visão estratégica.

            Escopo:
            - Dashboard do projeto e backlog com user stories
            - Monitoramento dos sensores (energia, temperatura, ocupação)
            - Análise e relatórios de performance com IA
            - Integração com sistemas de BI (Tableau/Power BI)

            Equipe:
            - Sponsor: Empresa Fictícia
            - Gerente de Projeto: Liang Yuan
            - Equipe Técnica: Ana, Maria, Caio, Linda

            Benefícios:
            - Decisão orientada por dados
            - Eficiência e economia
            - Prototipação rápida para a Era 4.0

            Riscos iniciais:
            - Integrações complexas com sensores
            - Confiabilidade dos dados simulados
            - Cronograma apertado
            """)

        if st.button("Gerar Project Charter", key="btn_charter"):
            charter = gerar_project_charter()
            st.markdown(charter)
            st.download_button("Baixar Project Charter (TXT)", charter, file_name="project_charter.txt")
            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica", 12)
            y = 750
            c.drawString(50, y, "Project Charter – Smart Office 4.0")
            y -= 30
            linhas = charter.split("\n")
            for linha in linhas:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, linha[:80])
                y -= 15
            c.save()
            buffer.seek(0)
            st.download_button("Baixar Project Charter (PDF)", buffer.getvalue(), file_name="project_charter.pdf", mime="application/pdf")

    elif aba == "Product Backlog Inicial":
        st.header("Product Backlog Inicial Gerado por IA")
        def gerar_backlog_inicial():
            data = [
                {"ID": 1, "User Story": "Como administrador, quero cadastrar salas para agendamentos.", "Sprint": 1, "Story Points": 8, "Status": "Pendente"},
                {"ID": 2, "User Story": "Como usuário, quero reservar salas pelo dashboard.", "Sprint": 1, "Story Points": 5, "Status": "Pendente"},
                {"ID": 3, "User Story": "Como gestor, quero visualizar burndown do projeto.", "Sprint": 2, "Story Points": 3, "Status": "Finalizado"},
                {"ID": 4, "User Story": "Como IoT admin, quero monitorar sensores em tempo real.", "Sprint": 2, "Story Points": 8, "Status": "Finalizado"},
                {"ID": 5, "User Story": "Como analista, quero cruzar dados de entregas com dados IoT.", "Sprint": 3, "Story Points": 5, "Status": "Em andamento"},
                {"ID": 6, "User Story": "Como PO, quero gerar relatórios automáticos via IA.", "Sprint": 4, "Story Points": 8, "Status": "Finalizado"}
            ]
            return pd.DataFrame(data)

        if st.button("Gerar Backlog Inicial", key="btn_backlog"):
            backlog = gerar_backlog_inicial()
            st.dataframe(backlog)

            backlog_txt = backlog.to_string(index=False)
            st.download_button("Baixar Backlog (TXT)", backlog_txt, file_name="product_backlog.txt")

            from reportlab.lib.pagesizes import letter, landscape
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=landscape(letter))
            c.setFont("Helvetica", 12)
            y = 500
            c.drawString(50, y+40, "Product Backlog Inicial – Smart Office 4.0")
            cols = backlog.columns.values
            y -= 20
            c.drawString(50, y, " | ".join([str(col) for col in cols]))
            y -= 20
            for _, row in backlog.iterrows():
                linha = " | ".join([str(row[col]) for col in cols])
                if y < 50:
                    c.showPage()
                    y = 500
                    c.setFont("Helvetica", 12)
                c.drawString(50, y, linha[:135])
                y -= 18
            c.save()
            buffer.seek(0)
            st.download_button("Baixar Backlog (PDF)", buffer.getvalue(), file_name="product_backlog.pdf", mime="application/pdf")

    elif aba == "Documentação":
        st.header("Documentação Final do Projeto")

        def gerar_documentacao():
            return textwrap.dedent("""\
            Documentação Final – Smart Office 4.0

            1. Resumo do Projeto:
            Plataforma web para gestão de escritório inteligente combinando backlog ágil, relatórios IA, monitoramento IoT (simulado) e integração com BI.

            2. Funcionalidades:
            - Dashboard Projeto: backlog, indicadores, velocidade, gestão de riscos.
            - Monitoramento IoT: leitura e histórico de sensores simulados (energia, temperatura).
            - Insights Estratégicos: storytelling cruzando dados do projeto e sensores.
            - Relatórios automáticos: geração e exportação (TXT/PDF) de status e lições aprendidas.
            - Project Charter: gerado na plataforma e disponível para download.
            - Product Backlog Inicial: modelado por IA, disponível para exportação.
            - Notebook Análise IoT: arquivo .ipynb incluso na entrega.
            - Links/Download para dashboards BI (exemplo: Tableau/Power BI, se aplicável).

            3. Estrutura de Pastas:
            - app.py                 # código principal Streamlit
            - reports.py, analysis.py, iot_simulation.py  # módulos
            - data/                  # arquivos csv simulados (backlog, iot)
            - requirements.txt       # dependências do projeto
            - iot_analysis.ipynb     # notebook de análise exploratória

            4. Execução:
            - Rodar “streamlit run app.py”
            - Navegar entre abas para acessar todas as funcionalidades e baixar documentos.
            - Notebook IoT pode ser aberto no Google Colab ou Jupyter.

            5. Observações/Sugestões:
            - Todos relatórios foram pensados para facilitar validação acadêmica e apresentação.
            - O modelo permite rápida adaptação para sensores reais.
            - Projeto focado em requisitos práticos e acadêmicos de Smart Office na Indústria 4.0.

            """)

        if st.button("Gerar Documentação Final", key="btn_doc"):
            doc = gerar_documentacao()
            st.markdown(doc)
            st.download_button("Baixar Documentação (TXT)", doc, file_name="documentacao_final.txt")

            from reportlab.lib.pagesizes import letter
            from reportlab.pdfgen import canvas
            from io import BytesIO
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica", 12)
            y = 750
            c.drawString(50, y, "Documentação Final – Smart Office 4.0")
            y -= 30
            linhas = doc.split("\n")
            for linha in linhas:
                if y < 50:
                    c.showPage()
                    y = 750
                c.drawString(50, y, linha[:105])
                y -= 15
            c.save()
            buffer.seek(0)
            st.download_button("Baixar Documentação (PDF)", buffer.getvalue(), file_name="documentacao_final.pdf", mime="application/pdf")
