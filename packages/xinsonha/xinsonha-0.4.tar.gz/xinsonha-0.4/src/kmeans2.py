
from __future__ import print_function
from pyspark.ml.clustering import KMeans
from pyspark.sql import SparkSession
 
"""
An example demonstrating k-means clustering.
Run with:
  bin/spark-submit examples/src/main/python/ml/kmeans_example.py
"""
 
if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("KMeansExample")\
        .getOrCreate()
 
    # Loads data.
    dataset = spark.read.format("libsvm")\
        .load("/usr/local/spark/data/mllib/sample_kmeans_data.txt")
 
    # Trains a k-means model.
    kmeans = KMeans().setK(2).setSeed(1)
    model = kmeans.fit(dataset)
 
    # Evaluate clustering by computing Within Set Sum of Squared Errors.
    wssse = model.computeCost(dataset)
    print("Within Set Sum of Squared Errors = " + str(wssse))
 
    # Shows the result.
    centers = model.clusterCenters()
    print("Cluster Centers: ")
    for center in centers:
        print(center)
    # $example off$
 
    spark.stop()


# Hierachy cluster
# from pyspark.ml.clustering import BisectingKMeans
# 
# spark = SparkSession\
#         .builder\
#         .appName("KMeansExample")\
#         .getOrCreate()
# # Loads data.
# dataset = spark.read.format("libsvm").load("/usr/local/spark/data/mllib/sample_kmeans_data.txt")
# 
# # Trains a bisecting k-means model.
# bkm = BisectingKMeans().setK(2).setSeed(1)
# model = bkm.fit(dataset)
# 
# # Evaluate clustering.
# cost = model.computeCost(dataset)
# print("Within Set Sum of Squared Errors = " + str(cost))
# 
# # Shows the result.
# print("Cluster Centers: ")
# centers = model.clusterCenters()
# for center in centers:
#     print(center)


# kmean low level
# from numpy import array
# from math import sqrt
# from pyspark import SparkConf, SparkContext
# from pyspark.mllib.clustering import KMeans, KMeansModel
#   
# # Configure the Spark environment
# sparkConf = SparkConf().setAppName("Classification").setMaster("local")
# sc = SparkContext(conf=sparkConf)
#   
# # Load and parse the data
# data = sc.textFile("/usr/local/spark/data/mllib/sample_kmeans_data.txt")
# parsedData = data.map(lambda line: array([float(x) for x in line.split(' ')]))
#   
# # Build the model (cluster the data)
# clusters = KMeans.train(
#     parsedData, 2, maxIterations=10, initializationMode="random")
#   
# # Evaluate clustering by computing Within Set Sum of Squared Errors
# def error(point):
#     center = clusters.centers[clusters.predict(point)]
#     return sqrt(sum([x**2 for x in (point - center)]))
#   
# WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
# print("Within Set Sum of Squared Error = " + str(WSSSE))
#   
# # Save and load model
# clusters.save(sc, "target/org/apache/spark/PythonKMeansExample/KMeansModel")
# sameModel = KMeansModel.load(sc, "target/org/apache/spark/PythonKMeansExample/KMeansModel")
