from pathlib import Path
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, desc
ROOT = Path(__file__).resolve().parents[1]
spark = SparkSession.builder.appName('Frame Anime Analysis').getOrCreate()
anime = spark.read.parquet(str(ROOT / 'output' / 'anime_clean'))
print('Total anime:', anime.count())
print('\nAnime by type:')
anime.groupBy('type').count().orderBy(desc('count')).show()
print('\nTop 10 highest-rated anime:')
anime.filter(anime.rating.isNotNull()).select('name','rating').orderBy(desc('rating')).show(10,truncate=False)
print('\nAverage rating by type:')
anime.groupBy('type').agg(avg('rating').alias('average_rating')).orderBy(desc('average_rating')).show()
spark.stop()
