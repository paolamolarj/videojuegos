from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lorsqu

def run_bigdata_pipeline():
    # 1. Inicializar la sesión de Spark
    spark = SparkSession.builder \
        .appName("GameMatch-DataPipeline") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()

    print("🚀 Sesión de Spark iniciada correctamente.")

    # Rutas de los datos (ajusta el nombre del archivo CSV según lo que descargues de Kaggle)
    raw_path = "raw/steam_reviews.csv"
    output_parquet_path = "processed/steam_data.parquet"

    # Nota: Si ejecutas esta fase de prueba sin haber descargado el CSV gigante todavía,
    # puedes simular el DataFrame para probar el flujo del pipeline.
    try:
        print(f"📥 Leyendo datos crudos desde {raw_path}...")
        df = spark.read.option("header", "true").option("inferSchema", "true").csv(raw_path)
        
        print(f"Total de registros crudos leídos: {df.count()}")

        # 2. Limpieza de datos (Data Cleaning)
        # Eliminamos filas con nulos en columnas críticas como user_id o app_id
        df_cleaned = df.dropna(subset=["user_id", "app_id"])

        # 3. Transformaciones opcionales (ej. estandarizar valores booleanos u horas)
        if "hours" in df_cleaned.columns:
            df_cleaned = df_cleaned.withColumn("hours", col("hours").cast("float"))

        print("⚙️ Datos limpiados y transformados con éxito.")

        # 4. Escritura en formato columnar Parquet (Optimización de Big Data)
        print(f"💾 Guardando dataset procesado en formato Parquet -> {output_parquet_path}...")
        df_cleaned.write.mode("overwrite").parquet(output_parquet_path)

        print("✅ Pipeline de Big Data ejecutado y almacenado en Parquet exitosamente.")

    except Exception as e:
        print(f"⚠️ Aviso: Para procesar los datos reales, coloca tu CSV de Kaggle en '{raw_path}'. Error actual: {e}")

    spark.stop()

if __name__ == "__main__":
    run_bigdata_pipeline()