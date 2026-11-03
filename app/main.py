
"""Ponto de entrada da API. Cria a aplicação, carrega e roda o modelo no ciclo de vida com suas rotas."""


from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.services import carregar_modelo

from app.routers import router

#Ciclo de vida: lido no disco uma vez. API ligando, guarda na memória para as requisições.
#Se o arquivo modelo falhar, a API sobe mesmo assim, mas sem modelo.
#Health = informação do problema e predict responde sem derrubar o serviço.

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.modelo = carregar_modelo()
        print("Modelo carregado na memória.")
    except Exception as erro:
        app.state.modelo = None
        print(f"Falha ao carregar o modelo: {erro}") #Roda para ligar e para desligar
    yield
    app.state.modelo = None
    print("API desligada, modelo liberado.")


app = FastAPI(
    title="PredictiveFactory IO",
    description="API de manutenção preditiva: prevê falha de máquinas a partir de dados de sensores.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router) #Aqui ficam as rotas