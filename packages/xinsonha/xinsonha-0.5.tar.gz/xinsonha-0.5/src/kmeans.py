
# kmean real example

from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import OneHotEncoder, StringIndexer, VectorAssembler
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline

# Configure the Spark environment
sparkConf = SparkConf().setAppName("Classification").setMaster("local")
sc = SparkContext(conf=sparkConf)

sqlContext = SQLContext(sc)

input = sqlContext.createDataFrame([
    ("a@email.com", 12000, "M"),
    ("b@email.com", 43000, "M"),
    ("c@email.com", 5000, "F"),
    ("d@email.com", 60000, "M")
]).toDF("email", "income", "gender")

indexer = StringIndexer().setInputCol("gender").setOutputCol("genderIndex")
encoder = OneHotEncoder().setInputCol("genderIndex").setOutputCol("genderVec")
assembler = VectorAssembler().setInputCols(["income", "genderVec"]).setOutputCol("features")
kmeans = KMeans().setK(2).setFeaturesCol("features").setPredictionCol("prediction") 
pipeline = Pipeline().setStages([indexer, encoder, assembler, kmeans])

kMeansPredictionModel = pipeline.fit(input)
print kMeansPredictionModel

predictionResult = kMeansPredictionModel.transform(input)
predictionResult.show()
