from tabulate import tabulate
from datetime import datetime
from agrupar_itens import agrupar_itens
from typing import List, Dict
from models import sessao, Cliente, Produto, Compra, Item
from sig_caixa import menu_sig


def ler_item(sessao, qtd_escolhida):
    """Lê um produto e quantidade a partir do ID informado pelo usuário."""

    escolha = input("ID do produto (Enter para fechar): ").strip()
    if escolha == "":
        return None

    if not escolha.isdigit():
        print("ID inválido.")
        return {}

    produto = sessao.get(Produto, int(escolha))
    if not produto:
        print("Produto não encontrado.")
        return {}

    qtd_str = input("Quantidade: ").strip()
    if not qtd_str.isdigit():
        print("Quantidade inválida.")
        return {}

    qtd = int(qtd_str)
    if qtd <= 0:
        print("Quantidade deve ser > 0.")
        return {}
    
    ja_escolhida = qtd_escolhida.get(produto.id_produto, 0)

    if ja_escolhida + qtd > produto.quantidade:
        disponivel = produto.quantidade - ja_escolhida
        print(
            f"Estoque insuficiente para {produto.nome}. "
            f"Já escolhido: {ja_escolhida}. "
            f"Disponível ainda: {max(disponivel, 0)}."
        )
        return {}

    return {
        "id_produto": produto.id_produto,
        "nome": produto.nome,
        "preco": float(produto.preco),
        "qtd": qtd,
        "total": float(produto.preco) * qtd,
    }

def criar_cliente():
    escolha = input("Informe o ID do cliente: ").strip()

    if not escolha.isdigit():
        print("ID inválido.")
        return criar_cliente()

    cliente = sessao.get(Cliente, int(escolha))

    if cliente:
        print(f"Cliente encontrado: {cliente.nome}")
        return cliente

    # não existe -> criar
    novo = Cliente(nome="") # nome temporário - é para evitar null
    sessao.add(novo)
    sessao.flush() # gera id_cliente
    novo.nome = f"Cliente {novo.id_cliente}"
    sessao.commit()

    print(f"Cliente criado: {novo.nome}")
    return novo

def nota_fiscal(cliente: Cliente, df_group):
    print("\n========================================== NOTA FISCAL ==========================================")
    print(f"Cliente: {cliente.nome} ")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    tabela = []
    for _, row in df_group.iterrows():
        tabela.append([
            int(row["id_produto"]),
            row["nome"],
            int(row["qtd"]),
            f"R$ {float(row['preco']):.2f}",
            f"R$ {float(row['total']):.2f}",
        ])

    print(tabulate(
        tabela,
        headers=["ID", "Produto", "Qtd", "Preço", "Total"],
        tablefmt="grid"
    ))

    total = float(df_group["total"].sum())
    print(f"Total: R$ {total:.2f}")
    print("====================================================================================================\n")

def registrar_compra(cliente: Cliente, df_group):
    compra = Compra(id_cliente=cliente.id_cliente)
    sessao.add(compra)
    sessao.flush() 

    for _, row in df_group.iterrows():
        novo_item = Item(
        id_compra=compra.id_compra,
        id_produto=row["id_produto"],
        quantidade=row["qtd"],
        preco=row["preco"],
        )

        sessao.add(novo_item)

        produto = sessao.get(Produto, int(row["id_produto"]))
        produto.quantidade -= int(row["qtd"])

    sessao.commit()
    return compra
    
def fazer_atendimento():
    cliente = criar_cliente()

    produtos = sessao.query(Produto).all()
    lista_produtos = [[p.id_produto, p.nome, p.preco, p.quantidade] for p in produtos]
    print("\n","="*35 + " PRODUTOS DISPONÍVEIS " + "="*34)
    print(tabulate(lista_produtos, headers=["ID", "Produto", "Preço", "Qtd"], tablefmt="grid"))

    itens: List[Dict] = []
    qtd_escolhida = {} 

    while True:
        item = ler_item(sessao, qtd_escolhida)

        if item is None:
            break # termina a escolha

        if item:
            itens.append(item)
            pid = item["id_produto"]
            qtd_escolhida[pid] = qtd_escolhida.get(pid, 0) + item["qtd"]

    if not itens:
        print("Nenhum item selecionado. Voltando ao menu inicial.")
        return
            
    # agrupar_itens.py 
    df_group = agrupar_itens(itens)
    registrar_compra(cliente, df_group)
    nota_fiscal(cliente, df_group)

def menu_caixa():
    while True:
        print("[1] Atendimento")
        print("[2] SIG")
        print("[0] Sair")
        opcao = input("Escolha: ")

        if not opcao.isdigit():
            print("Digite apenas números.\n")
            continue

        opcao = int(opcao)

        if opcao == 1:
            confirmar = input("\nIniciar atendimento? (s/n): ").lower().strip()
            if confirmar in ("s", "sim"):
                fazer_atendimento()
        elif opcao == 2:
            menu_sig()
        elif opcao == 0:
            print("Encerrando o programa.")
            break
        else:
            print("Digite apenas um número entre 0 e 2\n")

if __name__ == "__main__":
    menu_caixa()