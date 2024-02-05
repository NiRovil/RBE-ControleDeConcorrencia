from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class Transacao(Base):
    __tablename__ = 'transacoes'
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Integer)
    tipo = Column(String)
    descricao = Column(String)
    time_created = Column(DateTime(timezone=True), server_default=func.now())