from functools import lru_cache
from pyspark.sql import SparkSession
from pyspark.sql.functions import coalesce, col, lit
from app.config import CLEAN_DATA_PATH, RAW_DATA_PATH

@lru_cache(maxsize=1)
def get_spark():
    return (SparkSession.builder.appName('Frame Anime Data Studio').master('local[*]')
            .config('spark.ui.enabled', 'false').getOrCreate())

@lru_cache(maxsize=1)
def get_anime():
    spark = get_spark()
    if CLEAN_DATA_PATH.exists() and any(CLEAN_DATA_PATH.glob('*.parquet')):
        return spark.read.parquet(str(CLEAN_DATA_PATH))
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(f'Anime dataset not found at {RAW_DATA_PATH}')
    df = spark.read.option('header', True).option('inferSchema', True).csv(str(RAW_DATA_PATH)).dropDuplicates()
    for field in ('genre', 'type'):
        if field in df.columns:
            df = df.withColumn(field, coalesce(col(field), lit('Unknown')))
    return df

def json_number(value):
    if value is None: return None
    try:
        n = float(value)
        return n if n == n and abs(n) != float('inf') else None
    except (TypeError, ValueError): return None
