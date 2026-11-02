from typing import Literal

from pydantic import BaseModel, Field


class DadosMaquina(BaseModel):
    tipo: Literal["L", "M", "H"] = Field(
        description="Classe de qualidade da máquina: L (baixa), M (média) ou H (alta)"
    )
    temperatura_ar_k: float = Field(
        ge=273, le=323, description="Temperatura do ar, em Kelvin"
    )
    temperatura_processo_k: float = Field(
        ge=273, le=373, description="Temperatura do processo, em Kelvin"
    )
    velocidade_rotacao_rpm: float = Field(
        gt=0, le=5000, description="Velocidade de rotação, em RPM"
    )
    torque_nm: float = Field(
        ge=0, le=150, description="Torque, em Newton-metro"
    )
    desgaste_ferramenta_min: int = Field(
        ge=0, le=500, description="Tempo de uso da ferramenta, em minutos"
    )


class ResultadoPredicao(BaseModel):
    falha_prevista: int = Field(ge=0, le=1, description="1 = falha prevista, 0 = normal")
    probabilidade_falha: float = Field(ge=0, le=1, description="Probabilidade de falha, entre 0 e 1")
    mensagem: str = Field(description="Interpretação do resultado em texto")


class StatusSaude(BaseModel):
    status: str = Field(description="Situação do serviço")
    modelo_carregado: bool = Field(description="Se o modelo está na memória")