import streamlit as st
import pandas as pd
import plotly.express as px

# Configurar layout da página
st.set_page_config(layout="wide")

# Carregar dados
df = pd.read_csv(
    r"C:\Users\Gilson\Desktop\Projeto com PySpark\data\steam_cleaned.csv")

# Converter datas
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['year'] = df['release_date'].dt.year

# Categorizar por década


def categorize_decade(year):
    if pd.isna(year):
        return "Desconhecido"
    elif year < 2000:
        return "< 2000"
    elif year < 2010:
        return "2000s"
    elif year < 2020:
        return "2010s"
    else:
        return "2020s"


df['decade'] = df['year'].apply(categorize_decade)
df['is_free'] = df['price'] == 0
df['value_rating'] = df['positive_ratings'] / \
    df['price'].replace(0, float('nan'))

# Filtros únicos
all_tags = sorted(set(tag.strip()
                  for tags in df['steamspy_tags'].dropna() for tag in tags.split(';')))
decades = sorted(df['decade'].unique())

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

# Filtros
st.markdown("### 🔍 Filtros")
col_f1, col_f2 = st.columns([1, 2])
selected_decade = col_f1.selectbox("Filtrar por década:", decades)
selected_tag = col_f2.selectbox("Filtrar por categoria:", all_tags)

# Filtrar os dados
filtered = df[
    (df['decade'] == selected_decade) &
    (df['steamspy_tags'].str.contains(selected_tag, na=False))
]
top_10 = filtered.sort_values(by="positive_ratings", ascending=False).head(10)

# Gráficos lado a lado
col_top10, col_trend = st.columns(2)

with col_top10:
    st.subheader(
        f"🏆 Top 10 Jogos de '{selected_tag}' na Década {selected_decade}")
    st.dataframe(top_10[['name', 'developer', 'positive_ratings', 'price']])
    fig = px.bar(
        top_10,
        x='positive_ratings',
        y='name',
        color='price',
        orientation='h',
        title="Top 10 Avaliações Positivas",
        labels={'name': 'Jogo', 'positive_ratings': 'Avaliações Positivas'},
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

with col_trend:
    st.subheader("📈 Lançamentos por Ano")
    games_per_year = (
        df[df['year'].notna()]
        .groupby('year')
        .size()
        .reset_index(name='count')
    )
    fig_trend = px.line(
        games_per_year,
        x='year',
        y='count',
        title="Tendência de Lançamentos por Ano",
        markers=True,
        labels={'year': 'Ano', 'count': 'Quantidade de Jogos'}
    )
    st.plotly_chart(fig_trend, use_container_width=True)

# Linha de destaque: Gratuitos e Custo-benefício
st.markdown("---")
st.subheader("🎮 Destaques Especiais")
col_free, col_value = st.columns(2)

with col_free:
    st.markdown("🆓 **Top 10 Jogos Gratuitos Mais Populares**")
    top_free = df[df['is_free']].sort_values(
        by='positive_ratings', ascending=False).head(10)
    st.dataframe(top_free[['name', 'developer', 'positive_ratings']])

with col_value:
    st.markdown("💎 **Top 10 com Melhor Custo-Benefício**")
    top_value = df[df['price'] > 0].sort_values(
        by='value_rating', ascending=False).head(10)
    st.dataframe(
        top_value[['name', 'developer', 'positive_ratings', 'price', 'value_rating']])

# Rodapé
st.markdown("---")
st.caption("Criado por Gilson — Powered by Streamlit & Plotly")
