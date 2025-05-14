import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
df = pd.read_csv(
    r"C:\Users\Gilson\Desktop\Projeto com PySpark\data\steam_cleaned.csv")

# Título
st.title("🎮 Steam Games Dashboard")
st.markdown(
    "Análise interativa dos jogos da Steam com base em avaliações da comunidade.")

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric("💰 Preço Médio", f"${df['price'].mean():.2f}")
col2.metric("👍 Média Avaliações Positivas",
            f"{df['positive_ratings'].mean():,.0f}")
col3.metric("👎 Média Avaliações Negativas",
            f"{df['negative_ratings'].mean():,.0f}")

st.markdown("---")

# Filtro por Categoria (steamspy_tags)
all_tags = sorted(set(tag.strip()
                  for tags in df['steamspy_tags'].dropna() for tag in tags.split(';')))
selected_tag = st.selectbox("Selecione uma categoria:", all_tags)

# Filtrar os jogos com a tag selecionada
filtered = df[df['steamspy_tags'].str.contains(selected_tag, na=False)]

# Top 10 jogos mais bem avaliados nessa categoria
top_10 = (
    filtered
    .sort_values(by="positive_ratings", ascending=False)
    .head(10)
)

# Tabela com os top 10
st.subheader(f"🎯 Top 10 Jogos em: {selected_tag}")
st.dataframe(top_10[['name', 'developer', 'positive_ratings', 'price']])

# Gráfico de barras com Plotly
fig = px.bar(
    top_10,
    x='positive_ratings',
    y='name',
    color='price',
    orientation='h',
    title=f"Top 10 Jogos em '{selected_tag}' por Avaliações Positivas",
    labels={'name': 'Jogo', 'positive_ratings': 'Avaliações Positivas'},
    height=500
)
st.plotly_chart(fig, use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("Criado por Gilson — Powered by Streamlit & Plotly")
