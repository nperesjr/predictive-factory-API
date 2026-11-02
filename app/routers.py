from fastapi import APIRouter, HTTPException, Request

from app.schemas import DadosMaquina, ResultadoPredicao, StatusSaude
from app.services import prever

router = APIRouter()


@router.get("/health", response_model=StatusSaude, tags=["Monitoramento"])
def health(request: Request):
    modelo_carregado = request.app.state.modelo is not None
    return StatusSaude(
        status="ok" if modelo_carregado else "degradado",
        modelo_carregado=modelo_carregado,
    )


@router.post("/predict", response_model=ResultadoPredicao, tags=["Predição"])
def predict(dados: DadosMaquina, request: Request):
    modelo = request.app.state.modelo

    if modelo is None:
        raise HTTPException(
            status_code=500,
            detail="Modelo não está carregado. Tente novamente mais tarde.",
        )

    if dados.temperatura_processo_k <= dados.temperatura_ar_k:
        raise HTTPException(
            status_code=400,
            detail="A temperatura do processo deve ser maior que a temperatura do ar.",
        )

    try:
        falha, probabilidade = prever(modelo, dados)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro interno ao gerar a predição.",
        )

    if falha == 1:
        mensagem = "Falha prevista: agendar manutenção."
    else:
        mensagem = "Funcionamento normal."

    return ResultadoPredicao(
        falha_prevista=falha,
        probabilidade_falha=round(probabilidade, 4),
        mensagem=mensagem,
    )