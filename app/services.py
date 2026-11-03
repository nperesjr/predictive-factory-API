"""Camada de inferência que carrega o modelo e prevê de fato e pode ser usada em qualquer outra parte do sistema"""

from pathlib import Path

import joblib
import pandas as pd

from app.schemas import DadosMaquina


CAMINHO_MODELO = Path(__file__).resolve().parent.parent / "models" / "modelo.joblib" #montado a partir do app/ raiz models/ para funcionar para todo mundo (assim espero)


def carregar_modelo():
    return joblib.load(CAMINHO_MODELO) #chama no lifespan da main

#recebe modelo carregado e não lê disco
def prever(modelo, dados: DadosMaquina):
    entrada = pd.DataFrame([dados.model_dump()])
    falha = int(modelo.predict(entrada)[0])
    probabilidade = float(modelo.predict_proba(entrada)[0][1])
    return falha, probabilidade

#pipeline vai esperar uma tabela, não é o melhor dos mundos para diferentes formas de anotar as máquinas paradas, mas é um começo.