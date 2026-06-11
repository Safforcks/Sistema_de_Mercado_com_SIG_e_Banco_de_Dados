# Sistema de Mercado com SIG e Banco de Dados em Python

Projeto desenvolvido para a disciplina **Banco de Dados + Python**, com o objetivo de simular o funcionamento de um sistema de mercado integrado a um banco de dados relacional.

O sistema possui duas aplicações principais: um módulo de **Caixa**, responsável pelo registro das compras, e um **SIG — Sistema de Informações Gerenciais**, voltado para consultas, relatórios e gerenciamento de clientes, produtos e fornecedores.

---

## 1. Visão geral do projeto

O projeto foi desenvolvido em Python e utiliza banco de dados SQLite para armazenar informações relacionadas a clientes, produtos, fornecedores, compras e itens vendidos.

Além disso, o sistema utiliza bibliotecas como **Pandas** para tratamento e agrupamento de dados, leitura de arquivos CSV e Excel, e organização das informações antes de serem gravadas no banco.

O sistema contempla funcionalidades típicas de um ambiente comercial, como:

* Registro de compras;
* Controle de estoque;
* Geração de nota fiscal;
* Cadastro e consulta de produtos;
* Relatórios gerenciais;
* Análise de clientes e produtos;
* Integração com arquivos externos, como JSON, CSV e Excel.

---

## 2. Módulos principais

### 2.1 Caixa

O módulo de Caixa é responsável por realizar o atendimento ao cliente e registrar as compras no sistema.

Principais funcionalidades:

* Registro de compras de clientes;
* Agrupamento de itens iguais com Pandas;
* Atualização automática do estoque;
* Geração de nota fiscal;
* Armazenamento das informações no banco de dados.

As principais tabelas utilizadas nesse processo são:

* `compra`;
* `item`;
* `produto`;
* `cliente`.

---

### 2.2 SIG — Sistema de Informações Gerenciais

O SIG permite realizar consultas e análises sobre os dados armazenados no sistema.

O menu principal é dividido em duas áreas:

* Clientes;
* Produtos.

#### Funcionalidades relacionadas a clientes

* Listar clientes com compras;
* Listar clientes sem compras;
* Listar compras de um cliente específico;
* Consultar uma compra específica;
* Identificar clientes que mais compram;
* Identificar clientes que mais gastam.

#### Funcionalidades relacionadas a produtos

* Cadastrar produtos;
* Listar produtos;
* Atualizar produtos;
* Excluir produtos;
* Consultar produtos mais vendidos;
* Consultar produtos menos vendidos;
* Consultar produtos com estoque baixo;
* Consultar fornecedores de um produto;
* Consultar produtos com maior faturamento.

---

## 3. Estrutura dos arquivos

### `models.py`

Define as tabelas do banco de dados e seus relacionamentos.

Tabelas principais:

* `Cliente`;
* `Produto`;
* `Fornecedor`;
* `Produto_Fornecedores`;
* `Compra`;
* `Item`.

---

### `caixa.py`

Responsável pelo funcionamento do caixa.

Esse arquivo realiza:

* Atendimento do cliente;
* Registro da compra;
* Criação dos itens da compra;
* Baixa no estoque;
* Impressão da nota fiscal.

---

### `agrupar_itens.py`

Responsável por agrupar itens iguais utilizando Pandas.

Esse agrupamento evita duplicidade de produtos dentro da mesma compra e facilita o cálculo correto das quantidades e valores.

---

### `carregar_clientes.py`

Importa os clientes a partir do arquivo `clientes.json`.

O script evita duplicações e insere os dados na tabela `Cliente`.

---

### `web_scraping.py`

Realiza a extração de dados do site indicado no enunciado do projeto.

Após a coleta, o script gera o arquivo `produtos.csv`, que é utilizado posteriormente para carregar os produtos no banco de dados.

---

### `carregar_produtos.py`

Importa os produtos a partir do arquivo `produtos.csv`.

O arquivo utiliza Pandas para ler, tratar e gravar os dados na tabela `Produto`.

---

### `sig_caixa.py`

Arquivo principal do SIG.

Contém o menu inicial do Sistema de Informações Gerenciais e direciona o usuário para as áreas de clientes e produtos.

---

### `sig_clientes.py`

Contém as consultas e relatórios relacionados aos clientes.

Permite analisar o comportamento dos clientes com base nas compras registradas no sistema.

---

### `sig_produtos.py`

Contém as funcionalidades relacionadas aos produtos.

Inclui operações de CRUD, consultas gerenciais, análise de estoque, fornecedores e faturamento por produto.

---

### `carregar_excel.py`

Lê a planilha `fornecedores.xlsx`, que contém duas abas:

* `fornecedores`;
* `produtos-fornecedores`.

Esse arquivo é responsável por carregar os fornecedores e os relacionamentos entre produtos e fornecedores no banco de dados.

---

### `fornecedores.xlsx`

Planilha contendo os dados dos fornecedores e a relação N:N entre produtos e fornecedores.

---

### `modelagens.pdf`

Documento contendo a modelagem do banco de dados.

Inclui:

* Modelo Conceitual;
* Modelo Lógico;
* Modelo Físico.

---

### `mercado.db`

Banco de dados SQLite utilizado pelo sistema.

Contém os dados populados de clientes, produtos, fornecedores, compras e itens.

---

## 4. Como executar o projeto

### Registrar compras pelo caixa

```bash
python caixa.py
```

### Acessar o SIG

```bash
python sig_caixa.py
```

### Carregar fornecedores e associações

```bash
python carregar_excel.py
```

---

## 5. Consulta extra implementada

Além das funcionalidades principais, foi implementada a consulta:

**Produtos com maior faturamento**

Essa consulta calcula o faturamento total de cada produto com base na fórmula:

```text
preço × quantidade vendida
```

Com isso, o sistema permite identificar quais produtos geraram maior receita, contribuindo para uma análise gerencial mais completa.

---

## 6. Tecnologias utilizadas

* Python;
* SQLite;
* Pandas;
* JSON;
* CSV;
* Excel;
* Web Scraping;
* Modelagem de Banco de Dados.

---

## 7. Objetivo acadêmico

Este projeto tem finalidade acadêmica e foi desenvolvido para aplicar conceitos de Banco de Dados e Programação em Python.

Durante o desenvolvimento, foram trabalhados conceitos como:

* Criação e manipulação de banco de dados;
* Relacionamento entre tabelas;
* Consultas SQL;
* Processamento de dados com Pandas;
* Importação de dados externos;
* Organização modular do código;
* Desenvolvimento de relatórios gerenciais.

## Estrutura do Banco de Dados

O sistema utiliza um banco de dados SQLite chamado `mercado.db`, responsável por armazenar as informações de clientes, produtos, fornecedores, compras e itens vendidos.

A modelagem do banco foi organizada em três níveis:

* **Modelo Conceitual:** representa as principais entidades do sistema e seus relacionamentos;
* **Modelo Lógico:** define as tabelas, chaves primárias, chaves estrangeiras e relacionamentos;
* **Modelo Físico:** apresenta a implementação das tabelas em SQL.

A estrutura principal do banco é composta pelas seguintes tabelas:

| Tabela               | Finalidade                                                                            |
| -------------------- | ------------------------------------------------------------------------------------- |
| `cliente`            | Armazena os clientes cadastrados no sistema.                                          |
| `produto`            | Armazena os produtos disponíveis no mercado, incluindo preço e quantidade em estoque. |
| `fornecedor`         | Armazena os fornecedores dos produtos.                                                |
| `produto_fornecedor` | Representa o relacionamento N:N entre produtos e fornecedores.                        |
| `compra`             | Registra as compras realizadas pelos clientes.                                        |
| `item`               | Armazena os itens de cada compra, incluindo produto, quantidade e preço.              |

O relacionamento entre as tabelas permite registrar compras completas, controlar o estoque dos produtos e gerar consultas gerenciais no SIG.

## Demonstração do Módulo Caixa

O módulo **Caixa** permite registrar compras de clientes diretamente pelo terminal. Durante o atendimento, o sistema identifica o cliente pelo ID, lista os produtos disponíveis, permite selecionar os itens da compra, atualiza o estoque e gera a nota fiscal ao final do processo.

A imagem abaixo apresenta a tela de atendimento do caixa, com a listagem dos produtos disponíveis, seus respectivos preços e quantidades em estoque.

```markdown
![Tela de atendimento do caixa]()
```


Nessa etapa, o operador informa o ID do produto desejado e a quantidade comprada. O sistema registra os itens da compra e realiza automaticamente os controles necessários no banco de dados.


