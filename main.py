from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware, db

# importa o mapeamento e o modelo de dados
from schema import Transacao as SchemaTransacao, Cliente as SchemaCliente
from models import Transacao as ModelTransacao, Cliente as ModelCliente

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
    db_cliente.update({ModelCliente.saldo: ModelCliente.saldo + transacao.valor}, synchronize_session=False)

    # registra a transacao
    db_transacao = ModelTransacao(valor=transacao.valor, tipo=transacao.tipo, descricao=transacao.descricao, cliente_id=cliente_id)
    db.session.add(db_transacao)
    db.session.commit()

    return db_cliente

# endpoint para busca de extrato
@app.get("/clientes/{cliente_id}/extrato")
async def get_transacao(cliente_id: int):
    # com base em ORM faz a busca do extrato do cliente, com base em seu ID
    transacao = db.session.query(ModelTransacao).get(cliente_id)
    return transacao