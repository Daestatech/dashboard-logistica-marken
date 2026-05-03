import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚚 Central Logística Inteligente - Transferência entre Lojas")

file = st.file_uploader("Upload Relatório de Estoque por Loja", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    df.columns = [c.upper() for c in df.columns]

    # =========================
    # 🔴 FILTRO DE PRODUTOS
    # =========================
    palavras_bloqueadas = ("FLV", "BOVINO", "SUINO")

    df = df[~df['DESCCOMPLETA'].str.upper().str.startswith(palavras_bloqueadas, na=False)]

    st.info(f"📦 Produtos após filtro: {len(df)}")

    # =========================
    # 🔍 IDENTIFICAR LOJAS
    # =========================
    colunas = df.columns.tolist()
    pares = []

    for i in range(len(colunas)-1):
        if "EMPRESA" in colunas[i] and "ESTOQUE" in colunas[i+1]:
            pares.append((colunas[i], colunas[i+1]))

    # Converter estoque
    for _, est in pares:
        df[est] = pd.to_numeric(df[est], errors='coerce').fillna(0)

    # =========================
    # 🧠 LÓGICA LOGÍSTICA
    # =========================
    def analisar(row):
        estoques = {}

        for emp, est in pares:
            loja = str(row[emp])
            estoque = row[est]
            estoques[loja] = estoque

        loja_max = max(estoques, key=estoques.get)
        loja_min = min(estoques, key=estoques.get)

        excesso = estoques[loja_max]
        falta = estoques[loja_min]
        diferenca = excesso - falta

        if falta == 0 and excesso > 0:
            acao = f"🚨 Transferência URGENTE: {loja_max} → {loja_min}"
        elif diferenca > 20:
            acao = f"🔄 Redistribuir: {loja_max} → {loja_min}"
        else:
            acao = "✅ Equilibrado"

        return pd.Series([loja_max, loja_min, diferenca, acao])

    df[['LOJA_EXCESSO','LOJA_FALTA','DESEQUILIBRIO','ACAO']] = df.apply(analisar, axis=1)

    # =========================
    # 📊 KPIs
    # =========================
    st.subheader("📊 KPIs Logísticos")
    col1, col2, col3 = st.columns(3)

    col1.metric("Produtos analisados", len(df))
    col2.metric("Desequilíbrio total", int(df['DESEQUILIBRIO'].sum()))
    col3.metric("Transferências urgentes", df['ACAO'].str.contains("URGENTE").sum())

    # =========================
    # 🚨 PRIORIDADES
    # =========================
    st.subheader("🚨 Prioridades de Transferência")
    top = df.sort_values('DESEQUILIBRIO', ascending=False).head(20)

    st.dataframe(top[['DESCCOMPLETA','LOJA_EXCESSO','LOJA_FALTA','DESEQUILIBRIO','ACAO']])

    # =========================
    # 📈 GRÁFICO
    # =========================
    st.subheader("📈 Top Desequilíbrios")
    st.bar_chart(top.set_index('DESCCOMPLETA')['DESEQUILIBRIO'])

    # =========================
    # 📋 LISTA COMPLETA
    # =========================
    st.subheader("📋 Lista Completa")
    st.dataframe(df[['DESCCOMPLETA','LOJA_EXCESSO','LOJA_FALTA','DESEQUILIBRIO','ACAO']])