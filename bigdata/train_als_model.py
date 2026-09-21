from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

def train_als_recommender():
    # 1. Inicializar sesión de Spark
    spark = SparkSession.builder \
        .appName("GameMatch-ALS-Model") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()

    print("🤖 Iniciando entrenamiento del modelo ALS con PySpark...")

    parquet_path = "processed/steam_data.parquet"

    try:
        # 2. Leer los datos limpios almacenados en formato Parquet
        df = spark.read.parquet(parquet_path)
        
        # Asegurarnos de que las columnas críticas tengan el tipo de dato correcto
        # (user_id e app_id deben ser numéricos para ALS, o indexados previamente)
        # Nota: Si tu dataset usa IDs alfanuméricos, Spark MLlib requiere un StringIndexer previo.
        
        # 3. Configurar el Algoritmo ALS (Alternating Least Squares)
        als = ALS(
            maxIter=5,               # Número de iteraciones de entrenamiento
            regParam=0.01,           # Parámetro de regularización para evitar sobreajuste (overfitting)
            userCol="user_id",       # Columna identificadora de usuario
            itemCol="app_id",        # Columna identificadora del juego (item)
            ratingCol="hours",       # Columna de valor/interacción (ej. horas jugadas o puntuación)
            coldStartStrategy="drop" # Estrategia para manejar usuarios nuevos sin historial
        )

        # 4. Dividir en entrenamiento y prueba para evaluar el modelo
        (training, test) = df.randomSplit([0.8, 0.2])

        print("🔄 Entrenando el modelo ALS con los datos distribuidos...")
        model = als.fit(training)

        # 5. Evaluar el modelo con el conjunto de prueba (RMSE - Root Mean Square Error)
        predictions = model.transform(test)
        evaluator = RegressionEvaluator(metricName="rmse", labelCol="hours", predictionCol="prediction")
        rmse = evaluator.evaluate(predictions)
        print(f"📊 Modelo entrenado con éxito. Error Cuadrático Medio (RMSE): {rmse}")

        # 6. Generar el Top 10 de recomendaciones para todos los usuarios
        print("🎯 Generando el Top 10 de recomendaciones por usuario...")
        user_recs = model.recommendForAllUsers(10)
        
        # Guardar las recomendaciones generadas o el modelo entrenado para que FastAPI las consuma
        model.save("models/als_steam_model")
        print("✅ Modelo ALS guardado correctamente en la carpeta 'models/'.")

    except Exception as e:
        print(f"⚠️ Nota de ejecución: Asegúrate de tener el Parquet generado en la Fase 2. Detalle: {e}")

    spark.stop()

if __name__ == "__main__":
    train_als_recommender()