from fastapi import APIRouter

environment_router = APIRouter(prefix='/environment', tags=['environment'])

@environment_router.get('/')
async def home():
    '''
    Rota padrão do ambiente
    '''
    
    return {"msg":"rota padrão do ambiente"}