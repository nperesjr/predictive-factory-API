# PredictiveFactory IO


=============================================================

Olá, muito bom ter você aqui. Gostaria de avisar que os textos encontrados aqui foram estruturados através de IA generativa e revisados por este humano que vos fala e talvez, ele tenha esquecido de uma coisa ou outra. Se esse for o acaso, me avise. 

Obrigadooo 

=============================================================


API REST de manutenção preditiva. Recebe os dados dos sensores de uma máquina e responde se ela deve falhar, com a probabilidade estimada, permitindo que outros sistemas da fábrica consumam o modelo em tempo real.

## Problema de negócio

Em parques fabris, paradas não planejadas causadas por falhas mecânicas repentinas geram grandes prejuízos e atrasos nas entregas. O PredictiveFactory IO atua como um sistema de alerta precoce: a partir dos dados de sensores industriais, prevê se uma máquina vai quebrar (falha = 1) ou se está operando normalmente (falha = 0), para que a engenharia agende a manutenção antes da parada.

No projeto anterior, o modelo foi desenvolvido e avaliado em notebook. Neste projeto, ele é colocado em produção como uma API, pronta para ser consumida por painéis, aplicativos ou pelo próprio sistema de monitoramento.


## Origem do modelo

Este projeto reaproveita e aprimora o modelo de manutenção preditiva desenvolvido em um projeto anterior do curso (Opção A). 
A base é derivada do dataset disponível no exercício, com 10.000 registros de sensores.

Principais mudanças em relação ao projeto anterior:

- Pré-processamento e modelo empacotados em um único Pipeline do scikit-learn, para que a API receba dados crus.
- Balanceamento com `class_weight="balanced"` no lugar do SMOTENC, simplificando o deploy.
- Divisão em treino, validação e teste (60/20/20), estratificada.
- Remoção de identificadores e das colunas de modo de falha, que causariam vazamento de dados.

## Métricas do modelo

Modelo escolhido: Random Forest. Métricas no conjunto de teste, para a classe falha:

| Métrica | Valor |
|---|---|
| Recall | 0,603 |
| Precision | 0,732 |
| F1-score | 0,661 |
| ROC-AUC | 0,956 |

Foram comparados Regressão Logística e Random Forest, ambos com pesos de classe balanceados. A Regressão Logística encontrou um pouco mais de falhas, mas gerou cerca de 300 alarmes falsos a mais na validação, o que na prática faria a equipe parar máquinas saudáveis com frequência. O Random Forest teve F1 quase três vezes maior e melhor ROC-AUC, e foi o escolhido.

A acurácia não foi usada como critério: como apenas 3,4% das máquinas falham, um modelo que sempre responde “sem falha” já teria 96,6% de acurácia sem nenhuma utilidade.

Os detalhes estão em `notebooks/treino.ipynb`.

## Tecnologias

- Python 3.12
- FastAPI 0.162.0
- Uvicorn 0.54.0
- Pydantic 2.14.2
- scikit-learn 1.9.1
- pandas 3.1.0
- joblib 1.6.0

## Estrutura do projeto

```
app/
  main.py        ponto de entrada e ciclo de vida (lifespan)
  schemas.py     contratos de entrada e saída (Pydantic)
  services.py    carregamento do modelo e predição
  routers.py     rotas /health e /predict
data/            dataset
models/          modelo treinado (modelo.joblib)
notebooks/       treino e avaliação do modelo
```

## Como executar

Pré-requisitos: Python 3.12 e Git.

### Linux / macOS

```bash
git clone [link do seu repositório]
cd predictive-factory-API
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Em distribuições baseadas em Debian/Ubuntu, se a criação do ambiente virtual falhar, instale o módulo com `sudo apt install python3-venv` e repita o comando.

### Windows

```bash
git clone [link do seu repositório]
cd predictive-factory-API
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Com o servidor no ar, a documentação interativa fica em http://127.0.0.1:8000/docs


## Documentação da API

### GET /health

Informa se o serviço está no ar e se o modelo está carregado na memória.

```json
{"status": "ok", "modelo_carregado": true}
```

### POST /predict

Exemplo de requisição:

```json
{
  "tipo": "M",
  "temperatura_ar_k": 298.1,
  "temperatura_processo_k": 308.6,
  "velocidade_rotacao_rpm": 1551,
  "torque_nm": 42.8,
  "desgaste_ferramenta_min": 0
}
```

Exemplo de resposta:

```json

CODE: 200
Details:

{
  "falha_prevista": 0,
  "probabilidade_falha": 0,
  "mensagem": "Funcionamento normal."
}
Response headers
 content-length: 81 
 content-type: application/json 
 date: Mon,02 Nov 2026 21:30:23 GMT 
 server: uvicorn ]
```

Códigos de status:

| Código | Quando |
|---|---|
| 200 | predição realizada |
| 400 | temperatura do processo menor ou igual à do ar |
| 422 | campo com tipo inválido ou fora da faixa permitida |
| 500 | modelo não carregado ou erro interno |

## Vídeo de apresentação

[link do Google Drive]

## Melhorias futuras

- Ajuste do limiar de decisão: hoje o modelo indica falha quando a probabilidade passa de 50%. Reduzir esse limite aumentaria o recall, trocando algumas falhas não detectadas por alguns alarmes falsos a mais, troca que costuma valer a pena em manutenção.
- Aviso de valores fora do treino: a API aceita valores fisicamente plausíveis, mas alguns ficam fora da faixa vista no treino. A resposta poderia sinalizar quando a previsão é menos confiável.
- Sensores indisponíveis: os dados mostram que, às vezes, todos os sensores de uma máquina ficam fora do ar. Como o pipeline já preenche valores ausentes, a API poderia aceitar campos opcionais e ainda responder, em vez de exigir todos os valores.
- Testes automatizados: cobrir os casos 200, 400 e 422 com testes, para garantir que nada quebre a cada mudança.
- Monitoramento em produção: registrar as previsões para acompanhar se o comportamento das máquinas muda com o tempo e o modelo precisa ser retreinado.