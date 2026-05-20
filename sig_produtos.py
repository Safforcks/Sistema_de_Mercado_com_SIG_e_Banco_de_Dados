from tabulate import tabulate
from models import sessao, Produto, Fornecedor, Item


def criar_produto():
    print("\n","="*35 + " CADASTRAR PRODUTO " + "="*35)
    nome = input("Nome do produto: ").strip()
    if not nome:
        print("Nome não pode ser vazio.")
        return

    try:
        preco = float(input("Preço: ").strip().replace(",", "."))
        quantidade = int(input("Quantidade em estoque: ").strip())
    except ValueError:
        print("Valor inválido.")
        return

    produto = Produto(nome=nome, preco=preco, quantidade=quantidade)
    sessao.add(produto)
    sessao.flush()  # gera id_produto

    # associar fornecedores (opcional)
    associar_fornecedores_produto(produto)

    sessao.commit()
    print(f"Produto '{produto.nome}' cadastrado com ID {produto.id_produto}.")


def listar_produtos():
    print("\n", "="*35 + " LISTA DE PRODUTOS " + "="*35)
    produtos = sessao.query(Produto).all()

    if not produtos:
        print("Nenhum produto foi cadastrado.")
        return

    tabela = [
        [p.id_produto, p.nome, f"R$ {p.preco:.2f}", p.quantidade]
        for p in produtos
    ]
    print(tabulate(tabela, headers=["ID", "Nome", "Preço", "Qtd"], tablefmt="grid"))


def atualizar_produto():
    listar_produtos()
    pid = input("\nID do produto para atualizar: ").strip()
    if not pid.isdigit():
        print("ID inválido.")
        return

    produto = sessao.get(Produto, int(pid))
    if not produto:
        print("Produto não encontrado.")
        return

    print(f"\nAtualizando produto: {produto.nome}")

    novo_nome = input(f"Novo nome ({produto.nome}): ").strip()
    novo_preco = input(f"Novo preço ({produto.preco:.2f}): ").strip()
    nova_qtd = input(f"Nova quantidade ({produto.quantidade}): ").strip()

    if novo_nome:
        produto.nome = novo_nome
    if novo_preco:
        try:
            produto.preco = float(novo_preco.replace(",", "."))
        except ValueError:
            print("Preço inválido. Mantendo valor anterior.")
    if nova_qtd:
        try:
            produto.quantidade = int(nova_qtd)
        except ValueError:
            print("Quantidade inválida. Mantendo valor anterior.")

    opc = input("Deseja atualizar fornecedores deste produto? (s/n): ").lower().strip()
    if opc == "s":
        associar_fornecedores_produto(produto, substituir=True)

    sessao.commit()
    print("Produto atualizado com sucesso.")


def excluir_produto():
    listar_produtos()
    pid = input("\nID do produto para excluir: ").strip()
    if not pid.isdigit():
        print("ID inválido.")
        return

    produto = sessao.get(Produto, int(pid))
    if not produto:
        print("Produto não encontrado.")
        return

    # verificar se há itens associados (compras)
    if produto.itens:
        print("Não é possível excluir: produto possui itens em compras registradas.")
        return

    sessao.delete(produto)
    sessao.commit()
    print("Produto excluído com sucesso.")


def associar_fornecedores_produto(produto: Produto, substituir: bool = False):
    fornecedores = sessao.query(Fornecedor).all()
    if not fornecedores:
        print("Nenhum fornecedor cadastrado ainda.")
        return

    print("\n", "="*35 + " FORNECEDORES DISPONÍVEIS " + "="*35)
    tabela = [[f.id_fornecedor, f.nome] for f in fornecedores]
    print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="grid"))

    if substituir:
        produto.fornecedores.clear()

    ids = input("Informe IDs de fornecedores separados por vírgula (ou Enter para pular): ").strip()
    if not ids:
        return

    for fid in ids.split(","):
        fid = fid.strip()
        if not fid.isdigit():
            continue
        forn = sessao.get(Fornecedor, int(fid))
        if forn and forn not in produto.fornecedores:
            produto.fornecedores.append(forn)


def produtos_mais_vendidos():
    print("\n", "="*35 + " PRODUTOS MAIS VENDIDOS " + "="*35)

    # dicionário id_produto -> qtd total vendida
    vendas = {p.id_produto: 0 for p in sessao.query(Produto).all()}

    itens = sessao.query(Item).all()
    for it in itens:
        vendas[it.id_produto] = vendas.get(it.id_produto, 0) + it.quantidade

    # montar tabela com nome e quantidade vendida
    linhas = []
    for p in sessao.query(Produto).all():
        linhas.append([p.id_produto, p.nome, vendas.get(p.id_produto, 0)])

    # ordenar por qtd vendida desc
    linhas.sort(key=lambda x: x[2], reverse=True)

    print(tabulate(linhas, headers=["ID", "Produto", "Qtd vendida"], tablefmt="grid"))


def produtos_menos_vendidos():
    print("\n", "="*35 + " PRODUTOS MENOS VENDIDOS " + "="*35)

    vendas = {p.id_produto: 0 for p in sessao.query(Produto).all()}
    itens = sessao.query(Item).all()
    for it in itens:
        vendas[it.id_produto] = vendas.get(it.id_produto, 0) + it.quantidade

    linhas = []
    for p in sessao.query(Produto).all():
        linhas.append([p.id_produto, p.nome, vendas.get(p.id_produto, 0)])

    # ordenar por qtd vendida asc (menos vendidos primeiro)
    linhas.sort(key=lambda x: x[2])

    print(tabulate(linhas, headers=["ID", "Produto", "Qtd vendida"], tablefmt="grid"))


def produtos_estoque_baixo():
    print("\n", "="*35 + " PRODUTOS COM ESTOQUE BAIXO " + "="*35)
    limite = input("Informe o limite máximo de estoque (ex: 5): ").strip()
    try:
        limite = int(limite)
    except ValueError:
        print("Valor inválido.")
        return

    produtos = (
        sessao.query(Produto)
        .filter(Produto.quantidade <= limite)
        .all()
    )

    if not produtos:
        print("Nenhum produto com estoque baixo.")
        return

    tabela = [
        [p.id_produto, p.nome, p.quantidade]
        for p in produtos
    ]
    print(tabulate(tabela, headers=["ID", "Produto", "Estoque"], tablefmt="grid"))


def fornecedores_de_produto():
    listar_produtos()
    pid = input("\nID do produto: ").strip()
    if not pid.isdigit():
        print("ID inválido.")
        return

    produto = sessao.get(Produto, int(pid))
    if not produto:
        print("Produto não encontrado.")
        return

    if not produto.fornecedores:
        print("Este produto não possui fornecedores.")
        return

    print(f"\nFornecedores do produto: {produto.nome}")
    tabela = [[f.id_fornecedor, f.nome] for f in produto.fornecedores]
    print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="grid"))


def produtos_maior_faturamento():
    print("\n", "="*35+ " PRODUTOS COM MAIOR FATURAMENTO " + "="*35)

    # dicionário id_produto -> valor total vendido (preco * qtd)
    faturamento = {p.id_produto: 0.0 for p in sessao.query(Produto).all()}

    itens = sessao.query(Item).all()
    for it in itens:
        faturamento[it.id_produto] = faturamento.get(it.id_produto, 0.0) + (
            it.preco * it.quantidade
        )

    linhas = []
    for p in sessao.query(Produto).all():
        valor = faturamento.get(p.id_produto, 0.0)
        linhas.append([p.id_produto, p.nome, f"R$ {valor:.2f}"])

    # ordenar por faturamento desc
    linhas.sort(key=lambda x: float(x[2].replace("R$ ", "").replace(",", ".")), reverse=True)

    print(tabulate(linhas, headers=["ID", "Produto", "Faturamento"], tablefmt="grid"))



def menu_produtos():
    while True:
        print("\n============ MENU PRODUTOS ============")
        print("[1] Cadastrar produto")
        print("[2] Listar produtos")
        print("[3] Atualizar produto")
        print("[4] Excluir produto")
        print("[5] Produtos mais vendidos")
        print("[6] Produtos menos vendidos")
        print("[7] Produtos com estoque baixo")
        print("[8] Ver fornecedores de um produto")
        print("[9] Produtos com maior faturamento")
        print("[0] Voltar")

        escolha = input("Escolha: ").strip()

        if escolha == "1":
            criar_produto()
        elif escolha == "2":
            listar_produtos()
        elif escolha == "3":
            atualizar_produto()
        elif escolha == "4":
            excluir_produto()
        elif escolha == "5":
            produtos_mais_vendidos()
        elif escolha == "6":
            produtos_menos_vendidos()
        elif escolha == "7":
            produtos_estoque_baixo()
        elif escolha == "8":
            fornecedores_de_produto()
        elif escolha == "9":
            produtos_maior_faturamento()
        elif escolha == "0":
            break
        else:
            print("Opção inválida.")
