'''
Created on May 15, 2017

@author: atc
'''
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils
from pyspark import SparkConf, SparkContext

# Configure the Spark environment
sparkConf = SparkConf().setAppName("Classification").setMaster("local")
sc = SparkContext(conf = sparkConf)

# Load and parse the data file into an RDD of LabeledPoint.
data = MLUtils.loadLibSVMFile(
    sc, '/usr/local/spark/data/mllib/sample_libsvm_data.txt')
# Split the data into training and test sets (30% held out for testing)
(trainingData, testData) = data.randomSplit([0.7, 0.3])

# Train a DecisionTree model.
#  Empty categoricalFeaturesInfo indicates all features are continuous.
model = DecisionTree.trainClassifier(
    trainingData, numClasses=2, categoricalFeaturesInfo={},
    impurity='gini', maxDepth=5, maxBins=32
    )
# Evaluate model on test instances and compute test error
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
print labelsAndPredictions.collect()
testErr = labelsAndPredictions.filter(
    lambda (v, p): v != p).count() / float(testData.count()
    )
print('Test Error = ' + str(testErr))
print('Learned classification tree model:')
print(model.toDebugString())

# Save and load model
model.save(sc, "target/tmp/myDecisionTreeClassificationModel")
sameModel = DecisionTreeModel.load(sc, "target/tmp/myDecisionTreeClassificationModel")
