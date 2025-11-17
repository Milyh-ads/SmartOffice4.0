import pandas as pd
import numpy as np
import os
from datetime import datetime
import random

ARQUIVO_HIST = "data/iot_data.csv"

def gerar_dados_iot():
    dado = {
        "sala": random.choice(["Niterói", "Nova Iguaçu", "Centro"]),
        "temperatura": round(np.random.uniform(20, 26), 1),
        "energia": round(np.random.uniform(100, 300), 2),
        "ocupacao": random.randint(0, 1),
        "timestamp": datetime.now().isoformat(),
    }
    salvar_dado(dado)
    return dado

def salvar_dado(dado):
    df = pd.DataFrame([dado])
    if os.path.exists(ARQUIVO_HIST):
        df.to_csv(ARQUIVO_HIST, mode="a", header=False, index=False)
    else:
        df.to_csv(ARQUIVO_HIST, index=False)

def carregar_historico():
    if os.path.exists(ARQUIVO_HIST):
        df = pd.read_csv(ARQUIVO_HIST)
        return df
    else:
        return pd.DataFrame(columns=["sala", "temperatura", "energia", "ocupacao", "timestamp"])
