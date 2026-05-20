PROJETO DE BLOCO – TP5  
Aluno: Rainer Sacks De Almeida Caram Jaime
Disciplina: Banco de Dados + Python  

============================================================
1. Estrutura do projeto
============================================================
O projeto contém duas aplicações principais:

1) CAIXA

   - Registra compras de clientes
   - Agrupa itens com Pandas
   - Atualiza o estoque
   - Gera nota fiscal
   - Armazena dados em:
       • tabela compra
       • tabela item
       • tabela produto

2) SIG (Sistema de Informações Gerenciais)

   - Menu principal (Clientes / Produtos)
   - Funcionalidades de Clientes:
       • Clientes com compras
       • Clientes sem compras
       • Listar compras de um cliente
       • Consulta de compra específica
       • Clientes que mais compram
       • Clientes que mais gastam

   - Funcionalidades de Produtos:
       • CRUD de produtos
       • Produtos mais vendidos
       • Produtos menos vendidos
       • Produtos com estoque baixo
       • Fornecedores de um produto
       • Consulta extra: produtos com maior faturamento

============================================================
2. Arquivos
============================================================

models.py  
    Define todas as tabelas do banco:
    Cliente, Produto, Fornecedor, Produto_Fornecedores, 
    Compra, Item.

caixa.py  
    Realiza o atendimento do cliente, registra a compra, 
    gera itens, baixa estoque e imprime nota fiscal.

agrupar_itens.py  
    Responsável por agrupar os itens iguais usando Pandas.

carregar_clientes.py  
    Importa os clientes a partir do arquivo JSON “clientes.json”.
    Evita duplicações e insere na tabela Cliente.

web_scraping.py  
    Realiza scraping do site indicado no enunciado.
    Gera o arquivo “produtos.csv” utilizado no carregamento dos produtos
    no banco de dados.

carregar_produtos.py  
    Importa os produtos do arquivo CSV “produtos.csv”, gerado pelo
    web_scraping.py, utilizando Pandas e grava na tabela Produto.

sig_caixa.py  
    Menu principal do SIG.

sig_clientes.py  
    Consultas e relatórios relacionados a clientes.

sig_produtos.py  
    CRUD de produtos + consultas + fornecedores.

carregar_excel.py  
    Lê a planilha fornecedores.xlsx com duas abas:
        • fornecedores
        • produtos-fornecedores

fornecedores.xlsx  
    Planilha com dados dos fornecedores e relações N–N.

modelagens.pdf  
    Modelo conceitual, lógico e físico do banco.

mercado.db  
    Banco populado com produtos, fornecedores e compras.

modelagens.pdf  
  Contém:
    - Modelo Conceitual  
    - Modelo Lógico  
    - Modelo Físico  

============================================================
3. Como executar
============================================================

1) Para registrar compras:
   python caixa.py

2) Para acessar o SIG:
   python sig_caixa.py

3) Para carregar fornecedores e associações:
   python carregar_excel.py

============================================================
4. Consulta extra
============================================================

Foi implementada a consulta:
"Produtos com maior faturamento",
que soma o valor total vendido (preço × quantidade) de cada
produto, permitindo análise gerencial avançada.
