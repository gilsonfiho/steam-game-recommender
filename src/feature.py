import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv(data\steam.csv")

# Relação entre preço e número de avaliações positivas
plt.figure(figsize=(10, 6))
plt.scatter(df['price'], df['positive_ratings'], alpha=0.5, color='green')
plt.title('Preço vs Avaliações Positivas')
plt.xlabel('Preço')
plt.ylabel('Avaliações Positivas')
plt.show()

# Relação entre preço e avaliações negativas
plt.figure(figsize=(10, 6))
plt.scatter(df['price'], df['negative_ratings'], alpha=0.5, color='red')
plt.title('Preço vs Avaliações Negativas')
plt.xlabel('Preço')
plt.ylabel('Avaliações Negativas')
plt.show()
