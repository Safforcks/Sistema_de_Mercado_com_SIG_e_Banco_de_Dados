from sqlalchemy import (create_engine, Column, Integer, Float, String, ForeignKey, DateTime, Table)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

Base = declarative_base() # É a mãe de todas as tabelas

produto_fornecedor = Table(
    "produto_fornecedor", 
    Base.metadata, 
    Column("id_produto", ForeignKey("produto.id_produto"), primary_key=True),
    Column("id_fornecedor", ForeignKey("fornecedor.id_fornecedor"), primary_key=True)
    )

class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

    compras = relationship("Compra", back_populates="cliente")


class Produto(Base):
    __tablename__ = "produto"

    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)

    itens = relationship("Item", back_populates="produto")
    fornecedores = relationship(
        "Fornecedor",
        secondary=produto_fornecedor,
        back_populates="produtos"
    )


class Fornecedor(Base):
    __tablename__ = "fornecedor"

    id_fornecedor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)

    produtos = relationship(
        "Produto",
        secondary=produto_fornecedor,
        back_populates="fornecedores"
    ) 


class Compra(Base):
    __tablename__ = "compra"

    id_compra = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, default=datetime.now)

    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"))
    cliente = relationship("Cliente", back_populates="compras")

    itens = relationship("Item", back_populates="compra")

class Item(Base):
    __tablename__ = "item"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)

    id_compra = Column(Integer, ForeignKey("compra.id_compra"))
    id_produto = Column(Integer, ForeignKey("produto.id_produto"))

    compra = relationship("Compra", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")


engine = create_engine("sqlite:///mercado.db")
Sessao = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
sessao = Sessao()
Base.metadata.create_all(engine)
