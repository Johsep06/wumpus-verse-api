from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from dependencies import get_session, check_token
from schemas import ExecutionDBSchemas, UserSchemas, TurnSchemas
from models import ExecutionDB

execution_router = APIRouter(prefix='/execution', tags=['execution'])


@execution_router.get('/')
async def home(
    page: int = 1,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    offset = (page - 1) * limit
    return

@execution_router.post('/user')
async def save_execution(
    agent_id: int,
    environment_id: int,
    execution_schemas: list[TurnSchemas],
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    histor = [step.acao for step in execution_schemas]

    execution = ExecutionDB(
        id_agente=agent_id,
        id_ambiente=environment_id,
        user_id= user_schemas.id,
        posicao_x=execution_schemas[0].posicao_x,
        posicao_y=execution_schemas[0].posicao_y,
        qtd_ouros=execution_schemas[-1].ouros,
        wumpus=0,
        qtd_flechas=execution_schemas[-1].flechas,
        pontos=execution_schemas[-1].pontos,
        historico=','.join(histor)
    )

    session.add(execution)
    session.commit()
    return {
        'status_code': 200,
        'detail': 'execução salva com sucesso'
    }