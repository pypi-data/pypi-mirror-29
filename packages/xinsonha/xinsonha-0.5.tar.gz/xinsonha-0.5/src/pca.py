'''
Created on Jan 23, 2018

@author: khiem
'''
from pyspark import SparkConf, SparkContext
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.linalg.distributed import RowMatrix

# Configure the Spark environment
sparkConf = SparkConf().setAppName("PCA").setMaster("local")
sc = SparkContext(conf=sparkConf)


# row matrix
# rows = sc.parallelize([[1, 2], [1, 5]])
# mat = RowMatrix(rows)
# sims = mat.columnSimilarities()
# print sims.entries.first().value

# PCA
rows = sc.parallelize([
    Vectors.sparse(5, {1: 1.0, 3: 7.0}),
    Vectors.dense(2.0, 0.0, 3.0, 4.0, 5.0),
    Vectors.dense(4.0, 0.0, 0.0, 6.0, 7.0)
])

mat = RowMatrix(rows)
# Compute the top 4 principal components.
# Principal components are stored in a local dense matrix.
pc = mat.computePrincipalComponents(2)
print pc  # orth matrix

# Project the rows to the linear space spanned by the top 4 principal components.
projected = mat.multiply(pc)
print projected.rows.collect()

