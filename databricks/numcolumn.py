%python
from pyspark.sql.functions import mean, min, max
diamonds = spark.read.csv("/databricks-datasets/Rdatasets/data-001/csv/ggplot2/diamonds.csv", header="true", inferSchema="true")
diamonds.printSchema()
diamonds.select([mean('carat'), min('carat'), max('carat')]).show()
diamonds.count()
