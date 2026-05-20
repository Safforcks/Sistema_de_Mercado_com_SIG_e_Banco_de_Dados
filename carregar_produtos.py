import pandas as pd
from models import engine  

df = pd.read_csv("produtos.csv")
df.columns  = ["nome", "preco", "quantidade"]
df.to_sql("produto", engine, if_exists="append", index=False)
print("Produtos importados com sucesso!")