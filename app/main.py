import uvicorn

from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

# importa o mapeamento e o modelo de dados
from db.schema import Transacao as SchemaTransacao, Cliente as SchemaCliente
from db.models import Transacao as ModelTransacao, Cliente as ModelCliente

from datetime import datetime

import os
from dotenv import load_dotenv

# carrega a variavel de conexao com o db
load_dotenv('db.env')

app = FastAPI() # inicializa uma instancia da FastAPI
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL']) # elimina erro de csrf token

# endpoint base
@app.get("/")
def read_root():
    return {"Hello": "World"}

# endpoint para adicionar transacoes
@app.patch("/clientes/{cliente_id}/transacoes", response_model=SchemaCliente)
async def update_transacao(cliente_id: int, transacao: SchemaTransacao):

    # armazena o cliente
    db_cliente = db.session.query(ModelCliente).filter(ModelCliente.id == cliente_id).first()
    
    # se o cliente nao existir retorna um status 404
    if db_cliente is None:
        raise HTTPException(status_code=404, detail='Cliente not found!')

    # faz o update do saldo do cliente

    novo_saldo = db_cliente.saldo

    if transacao.tipo == 'c':
        novo_saldo -= transacao.valor

    elif transacao.tipo == 'd':
        novo_saldo += transacao.valor

    else:
        return db_cliente

    if novo_saldo > -db_cliente.limite :
        db_cliente.saldo = novo_saldo

        # registra a transacao
        db_transacao = ModelTransacao(valor=transacao.valor, tipo=transacao.tipo, descricao=transacao.descricao, cliente_id=cliente_id)
        db.session.add(db_transacao)
        db.session.commit()

        return db_cliente

    raise HTTPException(status_code=422, detail='Limit exceeded')

# endpoint para busca de extrato
@app.get("/clientes/{cliente_id}/extrato")
async def get_extrato(cliente_id: int):
    
    # busca as informacoes do cliente em questao
    cliente = db.session.query(ModelCliente).filter(ModelCliente.id == cliente_id).first()

    if cliente is None:
        raise HTTPException(status_code=404, detail='Client not found!')
    
    transacoes = db.session.query(ModelTransacao).filter(ModelTransacao.cliente_id == cliente_id).all()

    # cria uma lista com todos os lancamentos feitos pelo cliente
    transacao = [{"valor": item.valor, "tipo": item.tipo, "descricao": item.descricao, "realizada_em": item.time_created} for item in transacoes]
    
    return {
        "saldo": {
            "total": cliente.saldo,
            "data_extrato": datetime.now(),
            "limite": cliente.limite
        },
        "ultimas_transacoes": transacao
}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)