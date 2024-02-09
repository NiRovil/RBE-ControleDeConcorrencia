from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# cria uma base para os modelos de dados
Base = declarative_base()

# define a tabela de clientes
class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True, index=True)
    limite = Column(Integer)
    saldo = Column(Integer)

# define a tabela de transacoes
class Transacao(Base):
    __tablename__ = 'transacoes'
    id = Column(Integer, primary_key=True, index=True)
    valor = Column(Integer)
    tipo = Column(String(1))
    descricao = Column(String(10))
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    cliente_id = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship('Cliente')