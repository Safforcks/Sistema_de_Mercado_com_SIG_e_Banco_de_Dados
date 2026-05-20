import pandas as pd
from models import sessao, Fornecedor, Produto


def carregar_fornecedores(caminho_arquivo: str):
    df_f = pd.read_excel(caminho_arquivo, sheet_name="fornecedores")

    for _, x in df_f.iterrows():
        nome = str(x["nome"]).strip()
        if not nome:
            continue

        # evita duplicar pelo nome
        existente = sessao.query(Fornecedor).filter_by(nome=nome).first()
        if existente:
            continue

        forn = Fornecedor(nome=nome)
        sessao.add(forn)

    sessao.commit()
    print("Fornecedores carregados com sucesso.")


def carregar_produtos_fornecedores(caminho_arquivo: str):
    df_pf = pd.read_excel(caminho_arquivo, sheet_name="produtos-fornecedores")

    for _, x in df_pf.iterrows():
        try:
            id_prod = int(x["id_produto"])
            id_forn = int(x["id_fornecedor"])
        except (ValueError, TypeError):
            continue

        produto = sessao.get(Produto, id_prod)
        fornecedor = sessao.get(Fornecedor, id_forn)

        if not produto or not fornecedor:
            continue

        if fornecedor not in produto.fornecedores:
            produto.fornecedores.append(fornecedor)

    sessao.commit()
    print("Relações produto-fornecedor carregadas com sucesso.")


if __name__ == "__main__":
    caminho = "fornecedores.xlsx" 
    carregar_fornecedores(caminho)
    carregar_produtos_fornecedores(caminho)
