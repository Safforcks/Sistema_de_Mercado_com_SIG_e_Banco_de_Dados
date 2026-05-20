from sig_clientes import menu_clientes
from sig_produtos import menu_produtos

def menu_sig():
    while True:
        print("\n===== SIG — Sistema de Informações Gerenciais =====")
        print("[1] Clientes")
        print("[2] Produtos")
        print("[0] Sair")

        opcao = input("Escolha: ").strip()

        if opcao == "1":
            menu_clientes()
        elif opcao == "2":
            menu_produtos()
        elif opcao == "0":
            print("Saindo do SIG...\n")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu_sig()
