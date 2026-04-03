from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import desc

from dependencies import get_session, check_token
from schemas import ExecutionDBSchemas, UserSchemas, TurnSchemas
from models import ExecutionDB

execution_router = APIRouter(prefix='/execution', tags=['execution'])


def prepare_execution(execution_data) -> ExecutionDBSchemas:
    """
    Converte um objeto de dados de execução
    em um schema Pydantic `ExecutionDBSchemas` com o histórico processado.
    """
    histor_str: str = execution_data.historico
    histor_str = histor_str[2:]
    histor_list: list[str] = histor_str.split(',')
    histor_list = ['', *histor_list]

    qtd_passos = len(list(filter(lambda x: x.isupper(), histor_list)))

    execution = ExecutionDBSchemas(
        id=execution_data.id,
        user_id=execution_data.user_id,
        agente_id=execution_data.id_agente,
        ambiente_id=execution_data.id_ambiente,
        posicao_x=execution_data.posicao_x,
        posicao_y=execution_data.posicao_y,
        qtd_ouro=execution_data.qtd_ouros,
        qtd_flechas=execution_data.qtd_flechas,
        qtd_wumpus=execution_data.wumpus,
        pontos=execution_data.pontos,
        data=execution_data.data,
        historico=histor_list,
        qtd_passos=qtd_passos
    )

    return execution


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
        user_id=user_schemas.id,
        posicao_x=execution_schemas[0].posicao_x,
        posicao_y=execution_schemas[0].posicao_y,
        qtd_ouros=execution_schemas[-1].ouros,
        wumpus=execution_schemas[-1].kills,
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


@execution_router.get('/user')
async def get_execution_by_id(
    execution_id: int,
    session: Session = Depends(get_session),
):
    execution_data = session.query(ExecutionDB) \
        .filter(ExecutionDB.id == execution_id) \
        .first()

    if execution_data is None:
        return HTTPException(status_code=404, detail='Execução não encontrada')

    execution = prepare_execution(execution_data)

    return execution


@execution_router.delete('/user')
async def delete_execution(
    execution_id: int,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    execution_data = session.query(ExecutionDB) \
        .filter(ExecutionDB.id == execution_id) \
        .first()
    
    if execution_data is None:
        raise HTTPException(status_code=404, detail='Execução não encontrada')
    if user_schemas.id != execution_data.user_id:
        raise HTTPException(status_code=403, detail='O usuário não tem permisão para realizar essa ação')
    
    session.delete(execution_data)
    session.commit()
    return {
        'status_code': 200,
        'detail': 'Execução deletada com sucesso.',
    }


@execution_router.get('/list-user')
async def user_excutions(
    page: int = 1,
    limit: int = 5,
    agent_id: int = 0,
    enviroment_id: int = 0,
    session: Session = Depends(get_session),
    user_schemas: UserSchemas = Depends(check_token),
):
    
    offset = (page - 1) * limit
    
    # execution: list[ExecutionDB] = None
    
    if agent_id != 0 and enviroment_id != 0:
        execution = session.query(ExecutionDB) \
            .filter(ExecutionDB.id_ambiente == enviroment_id) \
            .filter(ExecutionDB.id_agente == agent_id) \
            .offset(offset)

    elif agent_id != 0:
        execution = session.query(ExecutionDB) \
            .filter(ExecutionDB.id_agente == agent_id) \
            .offset(offset)

    elif enviroment_id != 0:
        execution = session.query(ExecutionDB) \
            .filter(ExecutionDB.id_ambiente == enviroment_id) \
            .offset(offset)
    else:
        execution = session.query(ExecutionDB) \
            .filter(ExecutionDB.user_id == user_schemas.id) \
            .offset(offset)
    
    if execution is None:
        return HTTPException(
            status_code=404,
            detail='Não foram encontradas execuções que atendam ao padrão de busca informado'
        )
    
    executions = []
    for execution_db in execution:
        executions.append(prepare_execution(execution_db))

    
    return executions