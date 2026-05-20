from tabulate import tabulate
from models import sessao, Cliente, Compra, Item, Produto
from datetime import datetime


def clientes_com_compras():
    print("\n", "="*35 + " CLIENTES COM COMPRAS " + "="*35)

    clientes = (
        sessao.query(Cliente)
        .join(Compra)
        .group_by(Cliente.id_cliente)
        .all()
    )

    if not clientes:
        print("Nenhum cliente fez compras.")
        return

    tabela = [[c.id_cliente, c.nome] for c in clientes]
    print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="grid"))


def clientes_sem_compras():
    print("\n","="*35 + " CLIENTES SEM COMPRAS " + "="*35)

    clientes = (
        sessao.query(Cliente)
        .filter(~Cliente.compras.any())
        .all()
    )

    if not clientes:
        print("Todos os clientes possuem compras.")
        return

    tabela = [[c.id_cliente, c.nome] for c in clientes]
    print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="grid"))


def consultar_compras_cliente():
    cid = input("ID do cliente: ").strip()
    if not cid.isdigit():
        print("ID inválido.")
        return

    cliente = sessao.get(Cliente, int(cid))
    if not cliente:
        print("Cliente não encontrado.")
        return

    compras = (
        sessao.query(Compra)
        .filter_by(id_cliente=cliente.id_cliente)
        .order_by(Compra.data_hora.desc())
        .all()
    )

    if not compras:
        print("Este cliente não possui compras.")
        return

    tabela = []
    for compra in compras:
        itens = sessao.query(Item).filter_by(id_compra=compra.id_compra).all()
        total = sum(i.preco * i.quantidade for i in itens)

        tabela.append([
            compra.id_compra,
            compra.data_hora.strftime("%d/%m/%Y %H:%M"),
            f"R$ {total:.2f}"
        ])

    print("\n", "="*35 + " COMPRAS DO CLIENTE " + "="*35)
    print(f"Cliente: {cliente.nome}")
    print(tabulate(tabela, headers=["ID Compra", "Data/Hora", "Total"], tablefmt="grid"))

    escolha = input("\nDeseja consultar uma compra específica? (s/n): ").lower()
    if escolha == "s":
        consultar_compra_individual()


def consultar_compra_individual():
    cid = input("ID da compra: ").strip()
    if not cid.isdigit():
        print("ID inválido.")
        return

    compra = sessao.get(Compra, int(cid))
    if not compra:
        print("Compra não encontrada.")
        return

    itens = (
        sessao.query(Item, Produto)
        .join(Produto)
        .filter(Item.id_compra == compra.id_compra)
        .all()
    )

    tabela = []
    total = 0

    for item, prod in itens:
        subtotal = item.preco * item.quantidade
        total += subtotal
        tabela.append([
            prod.id_produto,
            prod.nome,
            item.quantidade,
            f"R$ {item.preco:.2f}",
            f"R$ {subtotal:.2f}",
        ])

    print("\n","="*35 + " DETALHES DA COMPRA " + "="*35)
    print(f"Compra: {compra.id_compra}")
    print(f"Cliente: {compra.cliente.nome}")
    print(f"Data: {compra.data_hora.strftime('%d/%m/%Y %H:%M')}")
    print(tabulate(tabela, headers=["ID", "Produto", "Qtd", "Preço", "Total"], tablefmt="grid"))
    print(f"TOTAL: R$ {total:.2f}")


def clientes_mais_compram():
    print("\n", "="*35 + " CLIENTES QUE MAIS COMPRAM " + "="*35)

    dados = (
        sessao.query(Cliente, Compra)
        .join(Compra)
        .all()
    )

    contagem = {}
    for cli, comp in dados:
        contagem[cli.nome] = contagem.get(cli.nome, 0) + 1

    tabela = [[nome, qtd] for nome, qtd in contagem.items()]
    tabela.sort(key=lambda x: x[1], reverse=True)

    print(tabulate(tabela, headers=["Cliente", "Nº compras"], tablefmt="grid"))


def clientes_mais_gastam():
    print("\n","="*35 + " CLIENTES QUE MAIS GASTAM " + "="*35)

    dados = (
        sessao.query(Cliente, Item).join(Cliente.compras).join(Compra.itens).all()
    )

    gastos = {}
    for cli, item in dados:
        gastos[cli.nome] = gastos.get(cli.nome, 0) + (item.preco * item.quantidade)

    tabela = [[cli, valor] for cli, valor in gastos.items()]
    tabela.sort(key=lambda x: x[1], reverse=True)

    for linha in tabela:
        linha[1] = f"R$ {linha[1]:.2f}"

    print(tabulate(tabela, headers=["Cliente", "Total gasto"], tablefmt="grid"))


def menu_clientes():
    while True:
        print("\n=========== MENU CLIENTES ===========")
        print("[1] Clientes com compras")
        print("[2] Clientes sem compras")
        print("[3] Consultar compras de um cliente")
        print("[4] Clientes que mais compram")
        print("[5] Clientes que mais gastam")
        print("[0] Voltar")

        op = input("Escolha: ").strip()

        if op == "1":
            clientes_com_compras()
        elif op == "2":
            clientes_sem_compras()
        elif op == "3":
            consultar_compras_cliente()
        elif op == "4":
            clientes_mais_compram()
        elif op == "5":
            clientes_mais_gastam()
        elif op == "0":
            break
        else:
            print("Opção inválida.")
