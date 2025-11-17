def criar_insights(df_iot, df_backlog):
    media_energia = df_iot["energia"].mean() if not df_iot.empty else 0
    total_pontos = df_backlog["story_points"].sum()

    texto = f"""
    Energia média consumida nas salas: {media_energia:.2f} kWh.
    Total de pontos planejados nas user stories: {total_pontos}.
    Sugestão: Analisar o impacto das funcionalidades na eficiência energética.
    """
    return texto
