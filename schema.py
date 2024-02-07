from pydantic import BaseModel

# define o mapeamento de um objeto no modelo
class Transacao(BaseModel):
    valor: int
    tipo: str
    descricao: str

    class Config:
        orm_mode = True