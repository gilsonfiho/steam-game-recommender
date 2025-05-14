from pyspark.sql.functions import col
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession
import pandas as pd
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv(r"C:\Users\Gilson\Desktop\Projeto com PySpark\data\steam.csv")

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


# Inicializando a sessão Spark
spark = SparkSession.builder.appName("SteamGameReview").getOrCreate()

# Convertendo o DataFrame pandas para PySpark DataFrame
spark_df = spark.createDataFrame(df)

# Mostrando as primeiras linhas
spark_df.show(5)


# Selecionando as colunas para a classificação (excluindo 'name' e 'total_ratings' que não são úteis para o modelo)
features = ['price', 'positive_ratings', 'negative_ratings', 'positive_ratio']
assembler = VectorAssembler(inputCols=features, outputCol="features")

# Aplicando o assembler no DataFrame
assembled_df = assembler.transform(spark_df)

# Preparando os dados para treino e teste
train_data, test_data = assembled_df.randomSplit([0.8, 0.2], seed=1234)

# Definindo a variável alvo 'is_positive'
train_data = train_data.withColumn('label', col('is_positive'))
test_data = test_data.withColumn('label', col('is_positive'))


# Criando o modelo Random Forest
rf = RandomForestClassifier(featuresCol='features', labelCol='label')

# Treinando o modelo
rf_model = rf.fit(train_data)

# Fazendo previsões no conjunto de teste
predictions = rf_model.transform(test_data)

# Avaliando o modelo
evaluator = BinaryClassificationEvaluator(labelCol='label')
accuracy = evaluator.evaluate(predictions)
print(f"Acurácia do modelo: {accuracy:.4f}")
