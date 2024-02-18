import uvicorn

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI, Depends,HTTPException

# importa o mapeamento e o modelo de dados
from db.schema import Transacao as SchemaTransacao, Cliente as SchemaCliente
from db.models import Transacao as ModelTransacao, Cliente as ModelCliente

from datetime import datetime

import os
from dotenv import load_dotenv

# carrega a variavel de conexao com o db
load_dotenv('db.env')

engine = create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = Session()

app = FastAPI() # inicializa uma instancia da FastAPI

# endpoint base
@app.get("/")
def read_root():
    return {"Hello": "World"}

# endpoint para adicionar transacoes
@app.post("/clientes/{cliente_id}/transacoes",response_model=SchemaCliente)
async def update_transacao(cliente_id: int, transacao: SchemaTransacao):

    # armazena o cliente com pessimist lock
    db_cliente = db.query(ModelCliente).filter_by(id=cliente_id).with_for_update().first()

    # se o cliente nao existir retorna um status 404
    if db_cliente is None:
        raise HTTPException(status_code=404, detail='Client not found!')
    
    # faz o update do saldo do cliente
    novo_saldo = db_cliente.saldo

    if transacao.tipo == 'd':
        novo_saldo -= transacao.valor

    elif transacao.tipo == 'c':
        novo_saldo += transacao.valor

    else:
        raise HTTPException(status_code=422, detail='Invalid data')

    if novo_saldo > -db_cliente.limite and len(transacao.descricao) <= 10:
        db_cliente.saldo = novo_saldo

        # registra a transacao
        db_transacao = ModelTransacao(valor=transacao.valor, tipo=transacao.tipo, descricao=transacao.descricao, cliente_id=cliente_id)
        db.add(db_transacao)
        db.commit()

        return db_cliente

    raise HTTPException(status_code=422, detail='Invalid data')

# endpoint para busca de extrato
@app.get("/clientes/{cliente_id}/extrato")
async def get_extrato(cliente_id: int):
    
    # busca as informacoes do cliente em questao
    db_cliente = db.query(ModelCliente).filter_by(id=cliente_id).with_for_update().first()

    if db_cliente is None:
        raise HTTPException(status_code=404, detail='Client not found!')
    
    transacoes = db.query(ModelTransacao).filter_by(id=cliente_id).with_for_update().all()

    # cria uma lista com todos os lancamentos feitos pelo cliente
    transacao = [{"valor": item.valor, "tipo": item.tipo, "descricao": item.descricao, "realizada_em": item.created_at} for item in transacoes]
    
    return {
        "saldo": {
            "total": db_cliente.saldo,
            "data_extrato": datetime.now(),
            "limite": db_cliente.limite
        },
        "ultimas_transacoes": transacao
}

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=3000, reload=True)