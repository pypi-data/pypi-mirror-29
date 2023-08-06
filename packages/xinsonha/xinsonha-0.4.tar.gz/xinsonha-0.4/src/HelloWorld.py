'''
Created on May 17, 2017

@author: atc
'''
# from pyspark.mllib.clustering import KMeans
from pyspark import SparkConf, SparkContext
from pyspark.mllib.util import MLUtils
import os

# Configure the Spark environment
sparkConf = SparkConf().setAppName("WordCounts").setMaster("local")
sc = SparkContext(conf = sparkConf)

from pyspark.mllib.feature import HashingTF
sentence = "hello hello world"
words = sentence.split()  # Split sentence into a list of terms
tf = HashingTF(10000)  # Create vectors of size S = 10,000
tf.transform(words)
print tf
rdd = sc.wholeTextFiles("data").map(lambda (name, text): text.split())
print rdd
tfVectors = tf.transform(rdd)   # Transforms an entire RDD
print tfVectors

from pyspark.mllib.linalg import Vectors
from pyspark.mllib.feature import StandardScaler
vectors = [Vectors.dense([-2.0, 5.0, 1.0]), Vectors.dense([2.0, 0.0, 1.0])]
print vectors
dataset = sc.parallelize(vectors)
scaler = StandardScaler(withMean=True, withStd=True)
model = scaler.fit(dataset)
result = model.transform(dataset)
print result.collect()

# from pyspark.mllib.regression import LabeledPoint 
# from pyspark.mllib.regression import LinearRegressionWithSGD 
# # points = dataset# (create RDD of LabeledPoint) 
# points = MLUtils.loadLibSVMFile(sc, '/usr/local/spark/data/mllib/sample_libsvm_data.txt')
# model = LinearRegressionWithSGD.train(points, iterations=200, intercept=True) 
# print "weights: %s, intercept: %s" % (model.weights, model.intercept) 

