# Sistema de Análise de Vendas — Etapa 1

## Sobre o projeto

Este projeto foi desenvolvido como parte do Trabalho de Conclusão de Curso de Análise e Desenvolvimento de Sistemas. O objetivo desta etapa é desenvolver um sistema para cadastrar e consultar vendas, permitindo também editar e excluir registros e visualizar informações básicas sobre as vendas realizadas.

A aplicação foi desenvolvida em Python e utiliza o Streamlit para a interface, SQLite para armazenar os dados e Pandas para organizar e analisar as informações.

## Funcionalidades

- Cadastro de vendas com nome do produto, quantidade, preço unitário e data.
- Cálculo automático do valor total de cada venda.
- Consulta das vendas cadastradas.
- Edição de registros existentes.
- Exclusão de vendas com confirmação.
- Exibição do faturamento acumulado, quantidade de vendas e ticket médio.
- Gráfico de faturamento por produto.
- Validação de campos e valores informados.

## Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento da aplicação.
- **Streamlit:** criação da interface web.
- **SQLite:** armazenamento dos registros de vendas.
- **Pandas:** organização dos dados e cálculo das informações utilizadas na análise.

## Como executar o projeto

### 1. Requisitos

- Python instalado.
- Arquivos do projeto disponíveis em uma mesma pasta.

### 2. Instalar as dependências

Abra o terminal na pasta do projeto e execute:

```bash
python -m venv .venv
```

No Windows PowerShell, ative o ambiente virtual:

```powershell
.\.venv\Scripts\Activate.ps1
```

Em seguida, instale as dependências:

```bash
python -m pip install -r requirements.txt
```

### 3. Iniciar a aplicação

Execute o comando:

```bash
python -m streamlit run app.py
```

O Streamlit disponibilizará o endereço local para acessar a aplicação no navegador.

## Como testar

1. Cadastre uma venda informando o produto, a quantidade, o preço unitário e a data.
2. Confira se a venda aparece na tabela e se o valor total foi calculado corretamente.
3. Verifique se os indicadores e o gráfico refletem os dados cadastrados.
4. Edite uma venda e confira se as alterações foram salvas.
5. Exclua uma venda e verifique se os demais registros continuam disponíveis.
6. Atualize a página e confira se os registros continuam salvos.

## Limitações

Esta versão é um protótipo acadêmico executado localmente. O sistema não possui autenticação de usuários nem está preparado para hospedagem em produção.

Os registros são armazenados no arquivo `vendas.db`. Para preservar os dados cadastrados, mantenha esse arquivo na pasta utilizada pelo projeto.

## Etapa 1

Esta etapa contempla as funcionalidades de cadastro, consulta, edição e exclusão de vendas, além da apresentação de indicadores básicos e do faturamento por produto.
