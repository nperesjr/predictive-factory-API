from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services import carregar_modelo


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.modelo = carregar_modelo()
        print("Modelo carregado na memória.")
    except Exception as erro:
        app.state.modelo = None
        print(f"Falha ao carregar o modelo: {erro}")
    yield
    app.state.modelo = None
    print("API desligada, modelo liberado.")


app = FastAPI(
    title="PredictiveFactory IO",
    description="API de manutenção preditiva: prevê falha de máquinas a partir de dados de sensores.",
    version="1.0.0",
    lifespan=lifespan,
)