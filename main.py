from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

# importa o mapeamento e o modelo de dados
from schema import Transacao as SchemaTransacao
from models import Transacao as ModelTransacao

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
@app.post("/clientes/{item_id}/transacoes", response_model=SchemaTransacao)
async def post_transacao(item_id: int, transacao: SchemaTransacao):
    # com base em ORM faz o lançamento da transacao no banco de dados Postgre
    db_transacao = ModelTransacao(id=item_id, valor=transacao.valor, tipo=transacao.tipo, descricao=transacao.descricao)
    db.session.add(db_transacao)
    db.session.commit()
    return db_transacao

# endpoint para busca de extrato
@app.get("/clientes/{item_id}/extrato")
async def get_transacao(item_id: int):
    # com base em ORM faz a busca do extrato do cliente, com base em seu ID
    transacao = db.session.query(ModelTransacao).get(item_id)
    return transacao