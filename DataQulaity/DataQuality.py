from pyspark.sql import SQLContext
sqlContext = SQLContext(sc)
sqlContext.count()
