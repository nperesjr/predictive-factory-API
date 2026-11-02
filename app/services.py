from pathlib import Path

import joblib
import pandas as pd

from app.schemas import DadosMaquina

CAMINHO_MODELO = Path(__file__).resolve().parent.parent / "models" / "modelo.joblib"


def carregar_modelo():
    return joblib.load(CAMINHO_MODELO)


def prever(modelo, dados: DadosMaquina):
    entrada = pd.DataFrame([dados.model_dump()])
    falha = int(modelo.predict(entrada)[0])
    probabilidade = float(modelo.predict_proba(entrada)[0][1])
    return falha, probabilidade