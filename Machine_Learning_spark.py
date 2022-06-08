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

#Pre-Load the classifier and the model
# Load the saved NaiveBayes Classifier
nb = NaiveBayes.load("static/resources/nb")

#Restored the trained predictor (Trained on 1 mil tweets)
predictor = NaiveBayesModel.load("static/resources/nb_model")

def eval_text_single(text, polarity = 1.0):
    list = [
    {"polarity": polarity, "text" : text}
    ]

    # The pipeline doesn't work as well when it it just one record in the list, so creating a fake list and adding the request to it.
    text_list = [{"text": "I am so happy for this text!  I can now have everything I want.", "polarity": 1.0},
             {"text": "This sucks!  I don't like this anymore.", "polarity": 0.0},
             {"text" : "This is a bad text.", "polarity" : 0.0},
             {"text": "I love you.", "polarity": 0.0},
             {"text": "Wow!  I can't believe how great this is.", "polarity": 0.0},
            ]
    
    # Add to the fake list
    text_list.append({"text" : text, "polarity" : polarity})
    
    tweet_df = spark.createDataFrame(text_list)

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
    #nb = NaiveBayes.load("static/resources/nb")

    #Restored the trained predictor (Trained on 1 mil tweets)
    #predictor = NaiveBayesModel.load("static/resources/nb_model")

    #Predict the sentiment of the text using the restored predictor
    test_results = predictor.transform(cleaned)

    df = test_results.select("text","prediction", "probability").toPandas()

    positives = [prob[1] for prob in df['probability']]
    df['probability'] = positives
    
    #Prepare the results, show the first row 
    result = {}
    result["text"] = df["text"][5]
    result["prediction"] = df["prediction"][5]
    result["probability"] = df["probability"][5]

    if result["prediction"] == 1:
        result["prediction"] = "Positive"
    else: 
        result["prediction"] = "Negative"

    return(result)

def eval_text_list(text_list):

    tweet_df = spark.createDataFrame(text_list)

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
    #nb = NaiveBayes.load("static/resources/nb")

    #Restored the trained predictor (Trained on 1 mil tweets)
    #predictor = NaiveBayesModel.load("static/resources/nb_model")

    #Predict the sentiment of the text using the restored predictor
    test_results = predictor.transform(cleaned)

    df = test_results.select("text", "tag", "prediction", "probability").toPandas()

    positive_score = [prob[1] for prob in df['probability']]
    
    df['probability'] = positive_score

    percents = ["{:.2%}".format(prob) for prob in df['probability']]
    df['percent'] = percents

    df.loc[df['prediction'] == 1.0, 'prediction'] = 'Positive'
    df.loc[df['prediction'] == 0.0, 'prediction'] = 'Negative'

    top_10 = df.sort_values(by=['probability'], ascending=False).head(10)
    bottom_10 = df.sort_values(by=['probability'], ascending=True).head(10)
    
    data = format_results_for_plotting(df)

    return(data, top_10.to_dict('records'), bottom_10.to_dict('records'))

def format_results_for_plotting(df):
    
    #df with the total count
    totals = df.groupby(['prediction']).size().reset_index(name='counts')

    #list with the distinct tags
    tags = df.groupby(['tag']).size().reset_index(name='counts')['tag'].to_list()

    #list with the distinct predictions
    predictions = df.groupby(['prediction']).size().reset_index(name='counts')['prediction'].to_list()

    # create a df with the aggregate counts
    agg_bytag = df.groupby(['tag','prediction']).size().reset_index(name='counts')


    #Create lists for the positive and negative counts
    positives = []
    negatives = []
    for tag in tags:
        for prediction in predictions:
            if prediction == "Positive":
                try:
                    pos = int(agg_bytag.loc[(agg_bytag["tag"] == tag) & (agg_bytag["prediction"] == prediction)]['counts'].values[0])
                except:
                    pos = int(0)
                positives.append(pos)
            if prediction == "Negative":
                try:
                    neg = int(agg_bytag.loc[(agg_bytag["tag"] == tag) & (agg_bytag["prediction"] == prediction)]['counts'].values[0]) 
                except:
                    neg = int(0)
                negatives.append(neg)

    #Create the dataset for the bar graph
    plot_data = {} 
    plot_data['tags'] = tags
    plot_data['positives'] = positives
    plot_data['negatives'] = negatives   

    #Create the full dataset for plotting
    data = {}
    data["plot_data"] = plot_data
    data["tags"] = tags
    data["totals"]={}
    data["totals"]["predictions"] = totals['prediction'].to_list()
    data["totals"]["counts"] = totals['counts'].to_list()
    data["total_count"] = int(totals['counts'].sum())
    data["positive_count"] = int(sum(positives))
    
    #return the plot information
    return(data)


