%python
from pyspark.sql.functions import mean, min, max, stddev

diamonds = spark.read.csv("/FileStore/tables/meseci.csv", header="true", inferSchema="true")
df = diamonds.dtypes
for i in range(len(df)):
  if df[i][1]=="string":
    diamonds.select(df[i][0]).distinct().show()
  else:
    diamonds.select([mean(df[i][0]), min(df[i][0]), max(df[i][0]), stddev(df[i][0])]).show()
