# Sistema de Análise de Vendas — Etapa 1

Aplicação web local desenvolvida em Python com Streamlit, SQLite e Pandas.

## Funcionalidades
- Cadastrar vendas com produto, quantidade, preço unitário e data.
- Calcular automaticamente o total de cada venda.
- Armazenar e consultar registros em SQLite.
- Editar vendas cadastradas.
- Excluir vendas com confirmação.
- Exibir faturamento acumulado, número de vendas, ticket médio e gráfico por produto.
- Validar campos obrigatórios e valores positivos.


## Teste de demonstração
1. Cadastrar um item 'x'
2. dar valor ao item
3. selecionar a quantidade e a data final
4. confirmar se o gráfico atualizou

## Tecnologias
- Streamlit: interface.
- SQLite: banco de dados.
- Pandas: consulta e agrupamento de dados.

## Limitações
Protótipo acadêmico local, sem autenticação ou hospedagem. O banco `vendas.db` deve ser mantido na pasta do projeto para preservar os registros.