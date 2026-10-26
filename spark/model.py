import os
from pathlib import Path
import joblib

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split


ROOT = Path(__file__).resolve().parents[1]

# =========================
# SPARK
# =========================

spark = SparkSession.builder \
    .appName("Anime Rating Prediction") \
    .master("local[*]") \
    .getOrCreate()


# =========================
# LOAD CLEAN DATA
# =========================

anime = spark.read.parquet(str(ROOT / "output" / "anime_clean"))


# =========================
# PREPARE DATA WITH SPARK
# =========================

data = anime \
    .withColumn(
        "episodes_num",
        col("episodes").cast("double")
    ) \
    .withColumn(
        "members_num",
        col("members").cast("double")
    )


data = data.filter(
    col("rating").isNotNull() &
    col("episodes_num").isNotNull() &
    col("members_num").isNotNull() &
    col("type").isNotNull()
)


# Convert Spark DataFrame to Pandas
pandas_data = data.select(
    "episodes_num",
    "members_num",
    "type",
    "rating"
).toPandas()


print("Training rows:", len(pandas_data))


# =========================
# FEATURES / TARGET
# =========================

X = pandas_data[
    [
        "episodes_num",
        "members_num",
        "type"
    ]
]

y = pandas_data["rating"]


# =========================
# TRAIN / TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print("Training:", len(X_train))
print("Testing:", len(X_test))


# =========================
# PREPROCESSING
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "type",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            ["type"]
        )
    ],
    remainder="passthrough"
)


# =========================
# RANDOM FOREST
# =========================

rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)


pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", rf)
    ]
)


# =========================
# TRAIN
# =========================

pipeline.fit(
    X_train,
    y_train
)


# =========================
# EVALUATION
# =========================

predictions = pipeline.predict(X_test)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

print("RMSE:", rmse)


# =========================
# SAVE MODEL
# =========================

os.makedirs(
    str(ROOT / "models"),
    exist_ok=True
)

joblib.dump(
    pipeline,
    str(ROOT / "models" / "anime_rating_model.pkl")
)


print("Model saved successfully!")
print(
    f"Location: {ROOT / 'models' / 'anime_rating_model.pkl'}"
)


spark.stop()