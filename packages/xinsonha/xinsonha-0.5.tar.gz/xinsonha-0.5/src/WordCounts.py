'''
Created on Apr 10, 2017

@author: atc
'''
# from pyspark.mllib.clustering import KMeans
from pyspark import SparkConf, SparkContext
import os

# Configure the Spark environment
sparkConf = SparkConf().setAppName("WordCounts").setMaster("local")
sc = SparkContext(conf = sparkConf)

# The WordCounts Spark program
textFile = sc.textFile(os.environ["SPARK_HOME"] + "/README.md")
wordCounts = textFile.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a+b)
print wordCounts.take(5)
# for wc in wordCounts.collect(): print wc

# difference map/flatMap
# print textFile.map(lambda x: x.split(" ")).collect()
# print textFile.flatMap(lambda x: x.split(" ")).collect()