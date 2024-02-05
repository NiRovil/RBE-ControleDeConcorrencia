from fastapi import FastAPI

app = FastAPI()

@app.post("/clientes/{item_id}/transacoes")
async def post_transacao(item_id: int):
    return {"item_id": item_id}