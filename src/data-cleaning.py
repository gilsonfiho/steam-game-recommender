import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv(data\steam.csv")

# Verificando as primeiras linhas para entender a estrutura
print(df.head())

# Verificando as colunas para entender quais estão disponíveis
print(df.columns)

# Adicionando a coluna 'is_positive' baseada na comparação entre as classificações positivas e negativas
df['is_positive'] = df['positive_ratings'] > df['negative_ratings']

# Convertendo a coluna 'is_positive' para 1 (positivo) e 0 (negativo)
df['is_positive'] = df['is_positive'].astype(int)

# Verificando a distribuição das avaliações (positivas e negativas)
print(df['is_positive'].value_counts())

# Visualizando a distribuição das avaliações (gráfico)
plt.figure(figsize=(6, 4))
df['is_positive'].value_counts().plot(kind='bar', color=['red', 'green'])
plt.title('Distribuição das Avaliações (Positiva vs Negativa)')
plt.ylabel('Contagem')
plt.xticks([0, 1], ['Negativa', 'Positiva'], rotation=0)
plt.show()

# Agora, o DataFrame tem uma coluna 'is_positive' para as avaliações
# Podemos salvar os dados limpos em um novo arquivo CSV
df.to_csv(
    r"C:\Users\Gilson\Desktop\Projeto com PySpark\data\steam_cleaned.csv", index=False)
