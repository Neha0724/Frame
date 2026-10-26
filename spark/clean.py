from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import coalesce, col, lit
ROOT = Path(__file__).resolve().parents[1]
spark = SparkSession.builder.appName('Frame Anime Data Cleaning').getOrCreate()
anime = spark.read.option('header', True).option('inferSchema', True).csv(str(ROOT / 'data' / 'anime.csv'))
anime = anime.dropDuplicates()
for field in ('genre', 'type'):
    if field in anime.columns: anime = anime.withColumn(field, coalesce(col(field), lit('Unknown')))
destination = ROOT / 'output' / 'anime_clean'
anime.write.mode('overwrite').parquet(str(destination))
print(f'Cleaned dataset saved to {destination}')
spark.stop()
