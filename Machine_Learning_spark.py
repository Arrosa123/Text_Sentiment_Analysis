import pandas as pd
from pyspark.sql import SparkSession
from pyspark import SparkFiles
from pyspark.ml.feature import Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer
from pyspark.sql.functions import length
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.linalg import Vector
from pyspark.ml import Pipeline
from pyspark.ml.classification import NaiveBayes, NaiveBayesModel

# Create the spark session
spark = SparkSession.builder.appName("Twitter_Sentiment_NLP").getOrCreate()

def eval_text_single(text):
    list = [
    {"text" : text}
    ]

    tweet_df = spark.createDataFrame(list)

    # Create a length column to be used as a future feature
    data_df = tweet_df.withColumn('length', length(tweet_df['text']))

    # Create all the features to the data set
    tokenizer = Tokenizer(inputCol="text", outputCol="token_text")
    stopRemove = StopWordsRemover(inputCol='token_text',outputCol='stop_tokens')
    hashingTF = HashingTF(inputCol="stop_tokens", outputCol='hash_token')
    idf = IDF(inputCol='hash_token', outputCol='idf_token')

    # Create feature vectors
    clean_up = VectorAssembler(inputCols=['idf_token', 'length'], outputCol='features')

    # Create and run a data processing Pipeline
    data_prep_pipeline = Pipeline(stages=[tokenizer, stopRemove, hashingTF, idf, clean_up])

    # Fit and transform the pipeline
    cleaner = data_prep_pipeline.fit(data_df)
    cleaned = cleaner.transform(data_df)

    # Load the saved NaiveBayes Classifier
    nb = NaiveBayes.load("static/resources/nb")

    #Restored the trained predictor (Trained on 1 mil tweets)
    predictor = NaiveBayesModel.load("static/resources/nb_model")

    #Predict the sentiment of the text using the restored predictor
    test_results = predictor.transform(cleaned)

    df = test_results.select("text","prediction", "probability").toPandas()

    #Prepare the results, show the first row 
    result = {}
    result["text"] = df["text"][0]
    result["prediction"] = df["prediction"][0]
    result["probability"] = df["probability"][0]

    if result["prediction"] == 1:
        result["prediction"] = "Positive"
    else: 
        result["prediction"] = "Negative"

    return(result)
    