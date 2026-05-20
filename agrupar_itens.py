import pandas as pd

def agrupar_itens(itens):

    df = pd.DataFrame(itens)

    if df.empty: # Se DataFrame for vazio, retorna True
        return df
    
    df_grupo = (df.groupby(["id_produto", "nome", "preco"], as_index=False).agg(qtd=("qtd", "sum"), total=("total", "sum")))

    return df_grupo