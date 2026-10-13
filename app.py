import sqlite3
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sistema de Análise de Vendas", page_icon="📊", layout="wide")
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
    conexao.commit()
    return conexao


def carregar_vendas():
    with conectar_banco() as conexao:
        return pd.read_sql_query(
            "SELECT id, produto, quantidade, preco_unitario, data_venda, total "
            "FROM vendas ORDER BY data_venda DESC, id DESC", conexao
        )


def moeda(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


conectar_banco().close()
st.title("📊 Sistema de Análise de Vendas")
st.caption("Etapa 1 — cadastro, consulta, edição e exclusão de vendas.")

st.header("Cadastrar venda")
with st.form("formulario_cadastro", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        produto = st.text_input("Produto", placeholder="Ex.: Teclado")
        quantidade = st.number_input("Quantidade", min_value=1, max_value=100000, value=1, step=1)
    with col2:
        preco = st.number_input("Preço unitário (R$)", min_value=0.01, max_value=100000000.0, value=100.00, step=1.00)
        data_venda = st.date_input("Data da venda", value=date.today())
    cadastrar = st.form_submit_button("Cadastrar venda", type="primary")

    if cadastrar:
        nome = produto.strip()
        if not nome:
            st.error("Informe o nome do produto.")
        elif quantidade < 1 or preco <= 0:
            st.error("Quantidade e preço devem ser maiores que zero.")
        else:
            total = int(quantidade) * float(preco)
            with conectar_banco() as conexao:
                conexao.execute(
                    """INSERT INTO vendas
                    (produto, quantidade, preco_unitario, data_venda, total)
                    VALUES (?, ?, ?, ?, ?)""",
                    (nome, int(quantidade), float(preco), data_venda.isoformat(), total)
                )
            st.success(f"Venda cadastrada! Total: {moeda(total)}")
            st.rerun()

vendas = carregar_vendas()
st.divider()
st.header("Vendas cadastradas")

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
        "total": "Total (R$)"
    })

    exibicao.insert(0, "Nº", range(1, len(exibicao) + 1))

    st.dataframe(exibicao, use_container_width=True, hide_index=True)


    st.subheader("Editar uma venda")
    opcoes = {
        f"ID {int(r.id)} — {r.produto} — {r.data_venda}": int(r.id)
        for r in vendas.itertuples(index=False)
    }
    escolha = st.selectbox("Selecione a venda para editar", list(opcoes.keys()))
    id_edicao = opcoes[escolha]
    atual = vendas.loc[vendas["id"] == id_edicao].iloc[0]

    with st.form("formulario_edicao"):
        c1, c2 = st.columns(2)
        with c1:
            produto_editado = st.text_input("Produto", value=str(atual["produto"]), key="produto_editado")
            quantidade_editada = st.number_input("Quantidade", min_value=1, max_value=100000, value=int(atual["quantidade"]), step=1, key="quantidade_editada")
        with c2:
            preco_editado = st.number_input("Preço unitário (R$)", min_value=0.01, max_value=100000000.0, value=float(atual["preco_unitario"]), step=1.00, key="preco_editado")
            data_editada = st.date_input("Data da venda", value=date.fromisoformat(str(atual["data_venda"])), key="data_editada")
        salvar = st.form_submit_button("Salvar alterações")
        if salvar:
            nome = produto_editado.strip()
            if not nome:
                st.error("O nome do produto não pode ficar vazio.")
            else:
                total = int(quantidade_editada) * float(preco_editado)
                with conectar_banco() as conexao:
                    conexao.execute(
                        """UPDATE vendas SET produto=?, quantidade=?, preco_unitario=?,
                        data_venda=?, total=? WHERE id=?""",
                        (nome, int(quantidade_editada), float(preco_editado), data_editada.isoformat(), total, id_edicao)
                    )
                st.success("Venda atualizada.")
                st.rerun()

   
st.subheader("Excluir uma venda")

with st.expander("Abrir opção de exclusão"):
    if vendas.empty:
        st.info("Não existem vendas para excluir.")
    else:
        opcoes_exclusao = {
            f"ID {int(r.id)} — {r.produto} — {r.data_venda}": int(r.id)
            for r in vendas.itertuples(index=False)
        }

        escolha_exclusao = st.selectbox(
            "Selecione a venda que deseja excluir",
            list(opcoes_exclusao.keys()),
            key="selecao_exclusao"
        )

        id_exclusao = opcoes_exclusao[escolha_exclusao]

        st.warning(
            f"A venda selecionada é a de ID {id_exclusao}. "
            "Essa ação não pode ser desfeita."
        )

        confirmar = st.checkbox(
            "Confirmo que desejo excluir esta venda",
            key="confirmar_exclusao"
        )

        if st.button(
            "Excluir venda selecionada",
            disabled=not confirmar,
            key="botao_excluir"
        ):
            with conectar_banco() as conexao:
                conexao.execute(
                    "DELETE FROM vendas WHERE id = ?",
                    (id_exclusao,)
                )

            st.success("Venda excluída com sucesso!")
            st.rerun()


st.divider()
st.header("Resumo geral")
vendas = carregar_vendas()
if vendas.empty:
    st.info("O resumo aparecerá após o primeiro cadastro.")
else:
    faturamento = float(vendas["total"].sum())
    numero_vendas = int(len(vendas))
    ticket_medio = faturamento / numero_vendas
    c1, c2, c3 = st.columns(3)
    c1.metric("Faturamento acumulado", moeda(faturamento))
    c2.metric("Vendas cadastradas", numero_vendas)
    c3.metric("Ticket médio", moeda(ticket_medio))
    por_produto = vendas.groupby("produto", as_index=False)["total"].sum().sort_values("total", ascending=False)
    por_produto = por_produto.rename(columns={"produto": "Produto", "total": "Faturamento (R$)"})
    st.subheader("Faturamento por produto")
    st.bar_chart(por_produto, x="Produto", y="Faturamento (R$)")
    st.caption("Os dados são armazenados localmente no arquivo vendas.db.")
