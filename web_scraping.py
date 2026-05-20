import csv
import requests
from bs4 import BeautifulSoup

URL = "https://pedrovncs.github.io/lindosprecos/produtos.html#"
pagina = requests.get(URL)
soup = BeautifulSoup(pagina.content, "html.parser")

lista_cartoes = soup.find(id="produtos-lista")
cartoes = lista_cartoes.find_all("div", class_="card-body")

with open("produtos.csv", "w") as arquivo:
    arquivo_csv = csv.writer(arquivo)
    arquivo_csv.writerow(["Produto", "Preço", "Quant."])

    for cartao in cartoes:
        titulo_tag = cartao.find("h5", attrs={"data-nome": True})
        titulo = titulo_tag["data-nome"].strip()

        preco_tag = cartao.find("p", attrs={"data-preco": True})
        preco = float(preco_tag["data-preco"].replace("R$", "").replace(",", ".").strip())

        qtd_tag = cartao.find("p", attrs={"data-qtd": True})
        qtd = int(qtd_tag["data-qtd"].strip())

        arquivo_csv.writerow([titulo, preco, qtd])
