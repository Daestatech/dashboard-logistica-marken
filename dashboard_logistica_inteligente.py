import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🚚 Central Logística Inteligente - Rede União Marken")

# =========================
# 📂 UPLOAD
# =========================
files = st.file_uploader(
    "Upload dos arquivos do ERP (.txt)",
    type=["txt"],
    accept_multiple_files=True
)

if files:

    lista_dfs = []

    # =========================
    # 📥 LEITURA
    # =========================
    for file in files:
        df = pd.read_csv(file, sep=";", encoding="latin1")
        df.columns = [c.upper() for c in df.columns]
        lista_dfs.append(df)

    # =========================
    # 🔗 MERGE
    # =========================
    df_final = lista_dfs[0]

    for df in lista_dfs[1:]:
        df_final = pd.merge(
            df_final,
            df,
            on=["COD_PROD", "DESCCOMPLETA"],
            how="outer",
            suffixes=("", "_2")
        )

    # =========================
    # 🔴 FILTRO POR PRODUTO
    # =========================
    palavras_bloqueadas = ("FLV", "BOVINO", "SUINO")

    df_final = df_final[
        ~df_final['DESCCOMPLETA'].str.upper().str.startswith(palavras_bloqueadas, na=False)
    ]

    # =========================
    # 🔴 FILTRO POR CATEGORIA
    # =========================
    categorias_bloqueadas = ("INSUMOS", "INSUMO E MATÉRIA PRIMA")

    colunas_nivel = [col for col in df_final.columns if "NIVEL_1" in col]

    for col in colunas_nivel:
        df_final = df_final[
            ~df_final[col].astype(str).str.upper().isin(categorias_bloqueadas)
        ]

    # =========================
    # 🔍 IDENTIFICAR LOJAS
    # =========================
    colunas = df_final.columns.tolist()
    pares = []

    for i in range(len(colunas)-1):
        if "EMPRESA" in colunas[i] and "ESTOQUE" in colunas[i+1]:
            pares.append((colunas[i], colunas[i+1]))

    # =========================
    # 🔢 TRATAR ESTOQUES
    # =========================
    for _, est in pares:
        df_final[est] = pd.to_numeric(df_final[est], errors='coerce').fillna(0)

    # =========================
    # ❌ REMOVER SEM ESTOQUE
    # =========================
    col_estoques = [est for _, est in pares]

    df_final['TOTAL_ESTOQUE'] = df_final[col_estoques].sum(axis=1)
    df_final = df_final[df_final['TOTAL_ESTOQUE'] > 0]

    st.success(f"📦 Produtos analisados: {len(df_final)}")

    # =========================
    # 🧠 LÓGICA
    # =========================
    def analisar(row):
        estoques = {}

        for emp, est in pares:
            loja = row[emp]
            estoque = row[est]

            if pd.notna(loja):
                estoques[str(loja)] = estoque

        if not estoques:
            return pd.Series([None, None, 0, "Sem dados"])

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

    df_final[['LOJA_EXCESSO','LOJA_FALTA','DESEQUILIBRIO','ACAO']] = df_final.apply(analisar, axis=1)

    # =========================
    # 📊 KPIs
    # =========================
    st.subheader("📊 KPIs")

    col1, col2, col3 = st.columns(3)

    col1.metric("Produtos analisados", len(df_final))
    col2.metric("Desequilíbrio total", int(df_final['DESEQUILIBRIO'].sum()))
    col3.metric("Transferências urgentes", df_final['ACAO'].str.contains("URGENTE").sum())

    # =========================
    # 🚨 PRIORIDADES
    # =========================
    st.subheader("🚨 Prioridades")

    top = df_final.sort_values('DESEQUILIBRIO', ascending=False).head(20)

    st.dataframe(top[['DESCCOMPLETA','LOJA_EXCESSO','LOJA_FALTA','DESEQUILIBRIO','ACAO']])

    # =========================
    # 📈 GRÁFICO
    # =========================
    st.bar_chart(top.set_index('DESCCOMPLETA')['DESEQUILIBRIO'])

    # =========================
    # 📋 BASE
    # =========================
    st.subheader("📋 Base completa")
    st.dataframe(df_final)