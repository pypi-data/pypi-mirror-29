'''
Created on Nov 21, 2017

@author: khiem
'''
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql import Row, Column
from pyspark.sql.functions import rand, randn, struct

# Configure the Spark environment
sparkConf = SparkConf().setAppName("Classification").setMaster("local")
sc = SparkContext(conf=sparkConf)

sqlContext = SQLContext(sc)

# data frame
lo = [('Ankit',25), ('Jalfaizy',22), ('saurabh',20), ('Bala',26)]
rdd = sc.parallelize(lo)
people = rdd.map(lambda x: Row(name=x[0], age=int(x[1])))
schemaPeople = sqlContext.createDataFrame(people)


# query
sqlContext.registerDataFrameAsTable(schemaPeople, 'train_table')
# temporary , exist with session
schemaPeople.createOrReplaceTempView("people")
# Register the DataFrame as a global temporary view
schemaPeople.createGlobalTempView("people")
# sql return dataFrame
sqlContext.sql('select name from train_table')  # .show(5)

# Random Data Generation
df = sqlContext.range(0, 4)
df.select(df.id, rand(2).alias("uniform"), randn(4).alias("standard normal"))\
#     .show()
print df  # note: no include uniform col ?

# Summary and Descriptive Statistics
df.describe(["id"]).show()
from pyspark.sql.functions import mean, min, max
df.select([mean("id"), min("id")])  # .show()

# Sample covariance and correlation
df = sqlContext.range(0, 5)\
    .withColumn("rand1", rand(6))\
    .withColumn("rand2", rand(8))
cor = df.stat.corr("rand1", "rand2"); print cor
cov = df.stat.cov('id', 'id')

# Cross Tabulation (Contingency Table)
names = ["Alice", "Bob", "Mike"]
items = ["milk", "bread", "butter", "apples", "oranges"]
df = sqlContext.createDataFrame(
    [(names[i % 3], items[i % 5]) for i in range(100)], ["name", "item"])

df.crosstab("name", "item").show()

# Frequent Items, support 40%
df = sqlContext.createDataFrame(
    [(1, 2, 3) if i % 2 == 0 else (i, 2 * i, i % 4)
     for i in range(10)], ["a", "b", "c"])
# df.show(12)
freq = df.stat.freqItems(["a", "b", "c"], 0.4)
# freq.show()
freq = df.withColumn('ab', struct('a', 'b')).stat.freqItems(['ab'], 0.4)
freq.show()

# Inferring the Schema Using Reflection
# Load a text file and convert each line to a Row.
lines = sc.textFile("/usr/local/spark/examples/src/main/resources/people.txt")
parts = lines.map(lambda l: l.split(","))
people = parts.map(lambda p: Row(name=p[0], age=int(p[1])))
schemaPeople = sc.createDataFrame(people)

# The schema is encoded in a string.
# schemaString = "name age"
# fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
# schema = StructType(fields)


