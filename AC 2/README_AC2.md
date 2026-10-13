# Sistema de Análise de Vendas — AC2

## Sobre o projeto

O Sistema de Análise de Vendas é uma aplicação desenvolvida em Python para auxiliar no gerenciamento de vendas e no controle de estoque de produtos.

Esta versão corresponde à **AC2**, dando continuidade ao desenvolvimento iniciado na AC1. Além de manter as funcionalidades de gerenciamento de vendas, o sistema agora conta com um módulo de controle de estoque.

## Funcionalidades

### Módulo de vendas
- Cadastro de vendas com produto, quantidade, preço unitário e data.
- Consulta das vendas registradas.
- Edição e exclusão de vendas.
- Exibição de indicadores, como faturamento total, quantidade de vendas e ticket médio.
- Gráfico de faturamento por produto.

### Módulo de estoque
- Cadastro de produtos e quantidades disponíveis.
- Definição do estoque mínimo de cada produto.
- Consulta e pesquisa de produtos cadastrados.
- Edição e exclusão de produtos.
- Identificação de produtos com estoque baixo ou esgotado.
- Armazenamento dos dados em banco de dados SQLite.

### Visão geral
- Exibição de indicadores de vendas e estoque.
- Visualização de informações relevantes para acompanhamento do sistema.

## Tecnologias utilizadas

- **Python:** linguagem de programação.
- **Streamlit:** criação da interface web.
- **SQLite:** armazenamento dos dados.
- **Pandas:** organização e apresentação dos dados.

## Requisitos

- Python instalado.
- Dependências listadas no arquivo `requirements.txt`.

## Como executar o projeto

1. Clone ou baixe o repositório.
2. Abra o terminal na pasta `AC2`.
3. Crie um ambiente virtual:

   ```bash
   python -m venv .venv
   ```

4. Ative o ambiente virtual no Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

6. Execute a aplicação:

   ```bash
   streamlit run app.py
   ```

7. Acesse o endereço local exibido no terminal.

## Banco de dados

O sistema utiliza SQLite para armazenar os registros de vendas e estoque. O banco de dados é criado ou atualizado pela aplicação conforme necessário.

O arquivo do banco de dados não precisa ser enviado ao GitHub para executar o projeto.

## Etapa do projeto

**AC2 — Controle de Estoque**

Esta etapa amplia o sistema desenvolvido na AC1, adicionando funcionalidades de cadastro, consulta, edição, exclusão e acompanhamento dos níveis de estoque.

## Autor

Desenvolvido como parte do projeto acadêmico Sistema de Análise de Vendas.
