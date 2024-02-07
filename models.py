from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# cria uma base para os modelos de dados
Base = declarative_base()

# define a tabela de dados
class Transacao(Base):
    __tablename__ = 'transacoes'
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Integer)
    tipo = Column(String)
    descricao = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())