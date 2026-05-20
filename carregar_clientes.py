import pandas as pd
from models import Sessao, Cliente 

def carregar_cliente():
    df = pd.read_json("clientes.json")

    with Sessao() as sessao:
        clientes_existentes = {c.nome for c in sessao.query(Cliente).all()} # É para evitar duplicar clientes

        for _, linha in df.iterrows():
            nome = linha["nome"]
            if nome in clientes_existentes:
                continue

            cliente = Cliente(nome=nome)
            sessao.add(cliente)

        sessao.commit()

if __name__ == "__main__":
    carregar_cliente()