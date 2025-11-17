def gerar_relatorio_status(kpis):
    return f"""
    Relatório de Status Simulado:
    Velocity média: {kpis['velocity']:.2f} pontos/sprint.
    Total de pontos planejados: {kpis['pontos_total']}.
    Todas as entregas seguem conforme o planejado. Não há grandes riscos identificados até o momento.
    """

def gerar_licoes_aprendidas():
    return (
        "Lições aprendidas simuladas: "
        "Planejamento detalhado dos requisitos facilita o sucesso ágil. "
        "A integração entre módulos IoT e análises BI gera maior valor para o projeto. "
        "Reúna a equipe periodicamente para revisões e ajustes."
    )
