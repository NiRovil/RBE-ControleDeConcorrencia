from pydantic import BaseModel

class Transacao(BaseModel):
    valor: int
    tipo: str
    descricao: str

    class Config:
        orm_mode = True