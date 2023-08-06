'''
Created on Apr 26, 2017

@author: atc
https://fullstackml.com/beginners-guide-apache-spark-machine-learning-scenario-with-a-large-input-dataset-1f0c6bc53f8f
https://fullstackml.com/beginners-guide-apache-spark-python-machine-learning-scenario-with-a-large-input-dataset-3fd1c319bbc

'''
import re
import pyspark
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark import SparkConf, SQLContext, SparkContext
 
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.mllib.evaluation import BinaryClassificationMetrics
 
targetTag = "java"
sparkConf = SparkConf().setAppName("StackExchange").setMaster("local")
sc = SparkContext(conf = sparkConf)
textFile = sc.textFile("/home/atc/data_src/Posts.small.xml")
sqlcontext = SQLContext(sc)
 
postsXml = textFile.map( lambda line: line.strip() ).\
    filter( lambda line: line != "<posts>" and line != "</posts>").\
    filter( lambda line: not line.startswith("<?xml version=") ).\
    filter( lambda line: line.find("Id=") >= 0 ).\
    filter( lambda line: line.find("Tags=") >= 0 ).\
    filter( lambda line: line.find("Body=") >= 0 ).\
    filter( lambda line: line.find("Title=") >= 0 )
 
postsRDD = postsXml.map( lambda s: pyspark.sql.Row(\
                Id = re.search('Id=".+?"', s).group(0)[4:-1].encode('utf-8'),\
                Label = 1.0 if re.search('Tags=".+?"', s) != None\
                            and re.search('Tags=".+?"', s).group(0)[6:-1].encode('utf-8').find(targetTag) >= 0 else 0.0,\
                Text = ((re.search('Title=".+?"', s).group(0)[7:-1] if re.search('Title=".+?"', s) != None else "") + \
                        " " + (re.search('Body=".+?"', s).group(0)[6:-1]) if re.search('Body=".+?"', s) != None else "")))
 
postsLabeled = sqlcontext.createDataFrame(postsRDD)
 
positive = postsLabeled.filter(postsLabeled.Label > 0.0)
negative = postsLabeled.filter(postsLabeled.Label < 1.0)
 
# Sample without replacement (False)
positiveTrain = positive.sample(False, 0.9)
negativeTrain = negative.sample(False, 0.9)
training = positiveTrain.unionAll(negativeTrain)
 
negTrainTmp1 = negativeTrain.withColumnRenamed("Label", "Flag")
negativeTrainTmp = negTrainTmp1.select(negTrainTmp1.Id, negTrainTmp1.Flag)
 
 
negativeTest = negative.join( negativeTrainTmp, negative.Id == negativeTrainTmp.Id, "LeftOuter").\
                        filter("Flag is null").\
                        select(negative.Id, negative.Text, negative.Label)
 
posTrainTmp1 = positiveTrain.withColumnRenamed("Label", "Flag")
positiveTrainTmp = posTrainTmp1.select(posTrainTmp1.Id, posTrainTmp1.Flag)
 
positiveTest = positive.join( positiveTrainTmp, positive.Id == positiveTrainTmp.Id, "LeftOuter").\
                        filter("Flag is null").\
                        select(positive.Id, positive.Text, positive.Label)
testing = negativeTest.unionAll(positiveTest)
 
 
# CREATE MODEL
numFeatures = 20000
numEpochs = 20
regParam = 0.02
 
tokenizer = Tokenizer().setInputCol("Text").setOutputCol("Words")
hashingTF = HashingTF().setNumFeatures(numFeatures).\
                setInputCol(tokenizer.getOutputCol()).setOutputCol("Features")
lr = LogisticRegression().setMaxIter(numEpochs).setRegParam(regParam).\
                                    setFeaturesCol("Features").setLabelCol("Label").\
                                    setRawPredictionCol("Score").setPredictionCol("Prediction")
pipeline = Pipeline().setStages([tokenizer, hashingTF, lr])
 
# this comand takes a time
model = pipeline.fit(training)
 
testTitle = "Easiest way to merge a release into one JAR file"
testBody = """Is there a tool or script which easily merges a bunch of 
    href=&quot;http://en.wikipedia.org/wiki/JAR_%28file_format%29&quot;
    &gt;JAR&lt;/a&gt; files into one JAR file? A bonus would be to easily set the main-file manifest 
    and make it executable. I would like to run it with something like:
    &lt;/p&gt;&#xA;&#xA;&lt;blockquote&gt;&#xA;  &lt;p&gt;java -jar 
    rst.jar&lt;/p&gt;&#xA;&lt;/blockquote&gt;&#xA;&#xA;&lt;p&gt;
    As far as I can tell, it has no dependencies which indicates that it shouldn't be an easy 
    single-file tool, but the downloaded ZIP file contains a lot of libraries."""
testText = testTitle + testBody
testDF = sqlcontext.createDataFrame([ ("0", testText, 1.0)], ["Id", "Text", "Label"])
result = model.transform(testDF)
prediction = result.collect()[0][7]
print("Prediction: ", prediction)
 
 
testingResult = model.transform(testing)
testingResultScores = testingResult.select("Prediction", "Label").rdd.map( lambda r: (float(r[0]), float(r[1])))
bc = BinaryClassificationMetrics(testingResultScores)
roc = bc.areaUnderROC
print("Area under the ROC:",  roc)
