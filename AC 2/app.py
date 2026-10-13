import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sistema de Análise de Vendas",
    page_icon="📊",
    layout="wide",
)

DB_PATH = Path(__file__).with_name("vendas.db")


def conectar_banco():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL CHECK (quantidade > 0),
            preco_unitario REAL NOT NULL CHECK (preco_unitario > 0),
            data_venda TEXT NOT NULL,
            total REAL NOT NULL CHECK (total > 0)
        )
    """)
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL COLLATE NOCASE UNIQUE,
            quantidade INTEGER NOT NULL DEFAULT 0 CHECK (quantidade >= 0),
            estoque_minimo INTEGER NOT NULL DEFAULT 0 CHECK (estoque_minimo >= 0),
            atualizado_em TEXT NOT NULL
        )
    """)
    conexao.commit()
    return conexao


def carregar_vendas():
    with conectar_banco() as conexao:
        return pd.read_sql_query(
            "SELECT id, produto, quantidade, preco_unitario, data_venda, total "
            "FROM vendas ORDER BY data_venda DESC, id DESC",
            conexao,
        )


def carregar_estoque():
    with conectar_banco() as conexao:
        return pd.read_sql_query(
            "SELECT id, produto, quantidade, estoque_minimo, atualizado_em "
            "FROM estoque ORDER BY produto COLLATE NOCASE",
            conexao,
        )


def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


conectar_banco().close()

st.title("📊 Sistema de Análise de Vendas")
st.caption("Controle de vendas e estoque em um só lugar.")

pagina = st.sidebar.radio(
    "Navegação",
    ["Visão geral", "Vendas", "Estoque"],
)
st.sidebar.divider()
st.sidebar.caption("Projeto acadêmico — Etapa 2")


if pagina == "Vendas":
    st.header("🛒 Vendas")
    st.caption("Cadastre, consulte, edite e exclua registros de vendas.")

    with st.expander("Cadastrar venda", expanded=True):
        with st.form("formulario_cadastro", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                produto = st.text_input("Produto", placeholder="Ex.: Teclado")
                quantidade = st.number_input(
                    "Quantidade vendida", min_value=1, max_value=100000, value=1, step=1
                )
            with col2:
                preco = st.number_input(
                    "Preço unitário (R$)", min_value=0.01,
                    max_value=100000000.0, value=100.00, step=1.00
                )
                data_venda = st.date_input("Data da venda", value=date.today())
            cadastrar = st.form_submit_button("Cadastrar venda", type="primary")

        if cadastrar:
            nome = produto.strip()
            if not nome:
                st.error("Informe o nome do produto.")
            else:
                total = int(quantidade) * float(preco)
                with conectar_banco() as conexao:
                    conexao.execute(
                        """INSERT INTO vendas
                        (produto, quantidade, preco_unitario, data_venda, total)
                        VALUES (?, ?, ?, ?, ?)""",
                        (nome, int(quantidade), float(preco), data_venda.isoformat(), total),
                    )
                st.success(f"Venda cadastrada! Total: {moeda(total)}")
                st.rerun()

    vendas = carregar_vendas()
    st.subheader("Vendas cadastradas")
    if vendas.empty:
        st.info("Nenhuma venda cadastrada. Use o formulário acima para começar.")
    else:
        exibicao = vendas.sort_values("id").copy()
        exibicao = exibicao.rename(columns={
            "id": "ID",
            "produto": "Produto",
            "quantidade": "Quantidade",
            "preco_unitario": "Preço unitário (R$)",
            "data_venda": "Data",
            "total": "Total (R$)",
        })
        exibicao.insert(0, "Nº", range(1, len(exibicao) + 1))
        st.dataframe(exibicao, use_container_width=True, hide_index=True)

        st.subheader("Editar uma venda")
        opcoes = {
            f"ID {int(r.id)} — {r.produto} — {r.data_venda}": int(r.id)
            for r in vendas.itertuples(index=False)
        }
        escolha = st.selectbox(
            "Selecione a venda para editar",
            list(opcoes.keys()),
            key="escolha_edicao_vendas",
        )
        id_edicao = opcoes[escolha]
        atual = vendas.loc[vendas["id"] == id_edicao].iloc[0]

        with st.form(f"formulario_edicao_venda_{id_edicao}"):
            c1, c2 = st.columns(2)
            with c1:
                produto_editado = st.text_input(
                    "Produto", value=str(atual["produto"]),
                    key=f"produto_editado_{id_edicao}",
                )
                quantidade_editada = st.number_input(
                    "Quantidade vendida", min_value=1, max_value=100000,
                    value=int(atual["quantidade"]), step=1,
                    key=f"quantidade_editada_{id_edicao}",
                )
            with c2:
                preco_editado = st.number_input(
                    "Preço unitário (R$)", min_value=0.01,
                    max_value=100000000.0, value=float(atual["preco_unitario"]),
                    step=1.00, key=f"preco_editado_{id_edicao}",
                )
                data_editada = st.date_input(
                    "Data da venda",
                    value=date.fromisoformat(str(atual["data_venda"])),
                    key=f"data_editada_{id_edicao}",
                )
            salvar = st.form_submit_button("Salvar alterações")

        if salvar:
            nome = produto_editado.strip()
            if not nome:
                st.error("O nome do produto não pode ficar vazio.")
            else:
                total = int(quantidade_editada) * float(preco_editado)
                with conectar_banco() as conexao:
                    conexao.execute(
                        """UPDATE vendas
                        SET produto=?, quantidade=?, preco_unitario=?,
                            data_venda=?, total=?
                        WHERE id=?""",
                        (nome, int(quantidade_editada), float(preco_editado),
                         data_editada.isoformat(), total, id_edicao),
                    )
                st.success("Venda atualizada.")
                st.rerun()

        with st.expander("Excluir uma venda"):
            opcoes_exclusao = {
                f"ID {int(r.id)} — {r.produto} — {r.data_venda}": int(r.id)
                for r in vendas.itertuples(index=False)
            }
            escolha_exclusao = st.selectbox(
                "Selecione a venda que deseja excluir",
                list(opcoes_exclusao.keys()),
                key="selecao_exclusao_vendas",
            )
            id_exclusao = opcoes_exclusao[escolha_exclusao]
            confirmar = st.checkbox(
                f"Confirmo a exclusão da venda ID {id_exclusao}",
                key="confirmar_exclusao_vendas",
            )
            if st.button(
                "Excluir venda selecionada",
                disabled=not confirmar,
                key="botao_excluir_venda",
            ):
                with conectar_banco() as conexao:
                    conexao.execute("DELETE FROM vendas WHERE id = ?", (id_exclusao,))
                st.success("Venda excluída.")
                st.rerun()


elif pagina == "Estoque":
    st.header("📦 Controle de estoque")
    st.caption("Cadastre produtos e acompanhe as quantidades disponíveis.")

    estoque = carregar_estoque()
    total_produtos = len(estoque)
    baixo = int((estoque["quantidade"] <= estoque["estoque_minimo"]).sum()) if not estoque.empty else 0
    unidades = int(estoque["quantidade"].sum()) if not estoque.empty else 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Produtos cadastrados", total_produtos)
    m2.metric("Unidades em estoque", unidades)
    m3.metric("Abaixo do mínimo", baixo)

    st.divider()
    col_cadastro, col_lista = st.columns([1, 1.5], gap="large")

    with col_cadastro:
        st.subheader("Cadastrar produto")
        with st.form("formulario_cadastro_estoque", clear_on_submit=True):
            nome_produto = st.text_input("Nome do produto", placeholder="Ex.: Teclado")
            quantidade_inicial = st.number_input(
                "Quantidade disponível", min_value=0, max_value=1000000, value=0, step=1
            )
            estoque_minimo = st.number_input(
                "Avisar quando chegar a", min_value=0, max_value=1000000, value=5, step=1
            )
            cadastrar_produto = st.form_submit_button("Adicionar ao estoque", type="primary")

        if cadastrar_produto:
            nome = nome_produto.strip()
            if not nome:
                st.error("Informe o nome do produto.")
            else:
                try:
                    with conectar_banco() as conexao:
                        conexao.execute(
                            """INSERT INTO estoque
                            (produto, quantidade, estoque_minimo, atualizado_em)
                            VALUES (?, ?, ?, ?)""",
                            (nome, int(quantidade_inicial), int(estoque_minimo), date.today().isoformat()),
                        )
                    st.success(f"Produto '{nome}' adicionado ao estoque.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Já existe um produto com esse nome no estoque.")

    with col_lista:
        st.subheader("Produtos cadastrados")
        busca = st.text_input("Pesquisar produto", placeholder="Digite o nome...")
        estoque_atual = carregar_estoque()
        if busca.strip():
            estoque_atual = estoque_atual[
                estoque_atual["produto"].str.contains(busca.strip(), case=False, na=False)
            ]

        if estoque_atual.empty:
            st.info("Nenhum produto encontrado. Cadastre um produto para começar.")
        else:
            tabela = estoque_atual.rename(columns={
                "id": "ID",
                "produto": "Produto",
                "quantidade": "Quantidade",
                "estoque_minimo": "Estoque mínimo",
                "atualizado_em": "Última atualização",
            }).copy()
            tabela.insert(0, "Nº", range(1, len(tabela) + 1))
            tabela["Situação"] = estoque_atual.apply(
                lambda r: "Esgotado" if int(r["quantidade"]) == 0
                else ("Estoque baixo" if int(r["quantidade"]) <= int(r["estoque_minimo"]) else "Normal"),
                axis=1,
            ).values
            st.dataframe(tabela, use_container_width=True, hide_index=True)

    st.divider()
    estoque_completo = carregar_estoque()
    if not estoque_completo.empty:
        st.subheader("Editar ou excluir produto")
        opcoes_produtos = {
            f"ID {int(r.id)} — {r.produto} ({int(r.quantidade)} unidades)": int(r.id)
            for r in estoque_completo.itertuples(index=False)
        }
        escolha_produto = st.selectbox(
            "Selecione um produto", list(opcoes_produtos.keys()), key="selecao_edicao_estoque"
        )
        id_produto = opcoes_produtos[escolha_produto]
        produto_atual = estoque_completo.loc[estoque_completo["id"] == id_produto].iloc[0]

        with st.form(f"formulario_edicao_estoque_{id_produto}"):
            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                nome_editado = st.text_input(
                    "Nome", value=str(produto_atual["produto"]),
                    key=f"nome_estoque_{id_produto}",
                )
            with ec2:
                qtd_editada = st.number_input(
                    "Quantidade disponível", min_value=0, max_value=1000000,
                    value=int(produto_atual["quantidade"]), step=1,
                    key=f"qtd_estoque_{id_produto}",
                )
            with ec3:
                minimo_editado = st.number_input(
                    "Estoque mínimo", min_value=0, max_value=1000000,
                    value=int(produto_atual["estoque_minimo"]), step=1,
                    key=f"minimo_estoque_{id_produto}",
                )
            salvar_produto = st.form_submit_button("Salvar alterações")

        if salvar_produto:
            nome = nome_editado.strip()
            if not nome:
                st.error("O nome do produto não pode ficar vazio.")
            else:
                try:
                    with conectar_banco() as conexao:
                        conexao.execute(
                            """UPDATE estoque
                            SET produto=?, quantidade=?, estoque_minimo=?, atualizado_em=?
                            WHERE id=?""",
                            (nome, int(qtd_editada), int(minimo_editado), date.today().isoformat(), id_produto),
                        )
                    st.success("Produto atualizado.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Já existe outro produto com esse nome.")

        with st.expander("Excluir produto"):
            st.warning("A exclusão remove o produto do cadastro de estoque.")
            confirmar_exclusao_produto = st.checkbox(
                f"Confirmo a exclusão de '{produto_atual['produto']}'",
                key=f"confirmar_exclusao_estoque_{id_produto}",
            )
            if st.button(
                "Excluir produto selecionado",
                disabled=not confirmar_exclusao_produto,
                key=f"botao_excluir_estoque_{id_produto}",
            ):
                with conectar_banco() as conexao:
                    conexao.execute("DELETE FROM estoque WHERE id=?", (id_produto,))
                st.success("Produto excluído do estoque.")
                st.rerun()


else:
    st.header("📈 Visão geral")
    st.caption("Resumo dos dados registrados no sistema.")

    vendas = carregar_vendas()
    estoque = carregar_estoque()

    faturamento = float(vendas["total"].sum()) if not vendas.empty else 0.0
    numero_vendas = int(len(vendas))
    ticket_medio = faturamento / numero_vendas if numero_vendas else 0.0
    produtos_estoque = len(estoque)
    unidades_estoque = int(estoque["quantidade"].sum()) if not estoque.empty else 0
    baixo = int((estoque["quantidade"] <= estoque["estoque_minimo"]).sum()) if not estoque.empty else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento acumulado", moeda(faturamento))
    c2.metric("Vendas cadastradas", numero_vendas)
    c3.metric("Ticket médio", moeda(ticket_medio))

    st.divider()
    e1, e2, e3 = st.columns(3)
    e1.metric("Produtos no estoque", produtos_estoque)
    e2.metric("Unidades disponíveis", unidades_estoque)
    e3.metric("Produtos no limite", baixo)

    if not vendas.empty:
        st.subheader("Faturamento por produto")
        por_produto = (
            vendas.groupby("produto", as_index=False)["total"]
            .sum()
            .sort_values("total", ascending=False)
            .rename(columns={"produto": "Produto", "total": "Faturamento (R$)"})
        )
        st.bar_chart(por_produto, x="Produto", y="Faturamento (R$)")
    else:
        st.info("Cadastre vendas para visualizar o gráfico de faturamento.")

    if not estoque.empty:
        st.subheader("Situação do estoque")
        estoque_grafico = estoque[["produto", "quantidade", "estoque_minimo"]].rename(
            columns={"produto": "Produto", "quantidade": "Quantidade", "estoque_minimo": "Estoque mínimo"}
        )
        st.dataframe(estoque_grafico, use_container_width=True, hide_index=True)

    st.caption("Os dados são armazenados localmente no arquivo vendas.db.")
