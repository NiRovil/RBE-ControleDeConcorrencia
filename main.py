from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db

from schema import Transacao as SchemaTransacao
from models import Transacao as ModelTransacao

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/clientes/{item_id}/transacoes", response_model=SchemaTransacao)
async def post_transacao(item_id: int, transacao: SchemaTransacao):
    db_transacao = ModelTransacao(valor=transacao.valor, tipo=transacao.tipo, descricao=transacao.descricao)
    db.session.add(db_transacao)
    db.session.commit()
    return db_transacao

@app.get("/clientes/{item_id}/extrato")
async def get_transacao(item_id: int):
    transacao = db.session.query(ModelTransacao).get(item_id)
    return transacao