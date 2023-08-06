'''
Created on Nov 26, 2017

@author: khiem
'''
from pyspark import SparkConf, SparkContext
from pyspark.ml.feature import StringIndexer
from pyspark import SQLContext

# Configure the Spark environment
sparkConf = SparkConf().setAppName("Classification").setMaster("local")
sc = SparkContext(conf=sparkConf)
sqlC = SQLContext(sc)

# StringIndexer
df = sqlC.createDataFrame(
    [(0, "a"), (1, "b"), (2, "c"), (3, "a"), (4, "a"), (5, "c")],
    ["id", "category"])
indexer = StringIndexer(inputCol="category", outputCol="indexer")
print indexer
print indexer.fit(df)
indexed = indexer.fit(df).transform(df)
indexed.show()

