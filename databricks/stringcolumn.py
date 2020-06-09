%python
from pyspark.sql.functions import mean, min, max
diamonds = spark.read.csv("/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", header="true", inferSchema="true")
diamonds.select("cut").distinct().show()
