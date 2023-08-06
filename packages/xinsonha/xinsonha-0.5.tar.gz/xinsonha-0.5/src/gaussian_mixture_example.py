
from __future__ import print_function
from pyspark.ml.clustering import GaussianMixture
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext

# Configure the Spark environment
sparkConf = SparkConf().setAppName("Classification").setMaster("local")
sc = SparkContext(conf=sparkConf)
"""
A simple example demonstrating Gaussian Mixture Model (GMM).
Run with:
  bin/spark-submit examples/src/main/python/ml/gaussian_mixture_example.py
"""

if __name__ == "__main__":
    spark = SparkSession\
        .builder\
        .appName("GaussianMixtureExample")\
        .getOrCreate()

    # $example on$
    # loads data
    dataset = spark.read.format("libsvm")\
        .load("/usr/local/spark/data/mllib/sample_kmeans_data.txt")

    gmm = GaussianMixture().setK(2).setSeed(538009335)
    model = gmm.fit(dataset)

    print("Gaussians shown as a DataFrame: ")
    model.gaussiansDF.show(truncate=False)
    # $example off$

    spark.stop()
