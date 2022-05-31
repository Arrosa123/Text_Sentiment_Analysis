#!/usr/bin/env python
# coding: utf-8


import sys

import h2o
import pandas as pd
import numpy as np
from scipy.stats import pearsonr #correlation
from sklearn.feature_extraction.text import TfidfVectorizer
import H2OGBMClassifier as hgb
from sklearn.metrics import roc_auc_score
import sys
from collections import defaultdict
import operator
#import sys

#reload(sys)  # Reload does the trick!
#sys.setdefaultencoding('utf-8')

#Dataset provided 
#file = './sentiment_m140_.csv'
#twitter_df = pd.read_csv(file)
#twitter_df = twitter_df.rename(columns={"target": "polarity", "ids": "id", "flag" : "query"})
#twitter_df["new_date"] = twitter_df["date"]

# 
# REPLACE WITH CODE TO ACCESS FROM S3
#
#Dataset Create
file = './static/resources/sentiment_analysis_10k.csv' 

def train_model(file):
    twitter_df = pd.read_csv(file,encoding = "ISO-8859-1")
    #
    #
    #



    print (twitter_df.shape)
    #Update the target to 0 or 1 -- came in as 0 or 4 
    twitter_df.loc[twitter_df["polarity"] == 4,"polarity"] = 1
    print (" average target is %f "  % np.mean(twitter_df["polarity"]))



    # Split up positive and negative tweets into two dataframes
    positive_tweets_df = twitter_df.loc[twitter_df["polarity"] ==1]
    negative_tweets_df = twitter_df.loc[twitter_df["polarity"] ==0]

    train_pos = positive_tweets_df[:int(len(positive_tweets_df)*0.8)]
    test_pos = positive_tweets_df[int(len(positive_tweets_df)*0.8):]
    train_neg = negative_tweets_df[:int(len(positive_tweets_df)*0.8)]
    test_neg = negative_tweets_df[int(len(positive_tweets_df)*0.8):]

    # combine positive and negative labels
    train_X = pd.concat([train_pos ,train_neg]) 
    test_X = pd.concat([test_pos ,test_neg])

    # create our target arrays
    train_y = train_X["polarity"]
    test_y = test_X["polarity"]


    # Remove the columns we're not using as features
    train_X.drop(["polarity"],inplace=True, axis=1)
    train_X.drop(["id"],inplace=True, axis=1)
    train_X.drop(["date"],inplace=True, axis=1)
    train_X.drop(["query"],inplace=True, axis=1)
    train_X.drop(["user"],inplace=True, axis=1)
    train_X.drop(["new_date"],inplace=True, axis=1)

    test_X.drop(["polarity"],inplace=True, axis=1)
    test_X.drop(["id"],inplace=True, axis=1)
    test_X.drop(["date"],inplace=True, axis=1)
    test_X.drop(["query"],inplace=True, axis=1)
    test_X.drop(["user"],inplace=True, axis=1)
    test_X.drop(["new_date"],inplace=True, axis=1)


    #tf-idf model
    tfv=TfidfVectorizer(min_df=0, max_features=3000, strip_accents='unicode',lowercase =True,
                                analyzer='word', token_pattern=r'\w{3,}', ngram_range=(1,1),
                                use_idf=True,smooth_idf=True, sublinear_tf=True, stop_words = "english")   
    #h2o gbm model
    model=hgb.H2OGBMClassifier (ntrees=100,
                                learn_rate=0.1,
                                distribution="bernoulli",
                                col_sample_rate=1.0,
                                col_sample_rate_per_tree =0.5,
                                nthread=15,
                                sample_rate=0.9,
                                stopping_metric="logloss",
                                nbins=255,
                                min_rows=1,
                                ram="20G",
                                max_depth=4,
                                seed=1)

    #apply tf idf
    data=tfv.fit_transform(train_X["text"].to_numpy())
    data=data.toarray()
    print (data.shape) 


    test_data = tfv.fit_transform(test_X["text"].to_numpy())
    test_data = test_data.toarray()
    print(test_data.shape)



    #fit model
    model.fit(data,np.array(train_y)) # feed target



    #make predictions)probabilities) on tweets
    preds=model.predict_proba(test_data)[:,1]


    print ("training auc is %f" %roc_auc_score(test_y,preds) )



    from sklearn.ensemble import GradientBoostingClassifier

    # Create a classifier object
    learning_rates = [0.1]
    for learning_rate in learning_rates:
        classifier = GradientBoostingClassifier(n_estimators=100,
                                                learning_rate=learning_rate,
                                                max_features=20,
                                                max_depth=4)

        # Fit the model
        classifier.fit(data, train_y)
        print("Learning rate: ", learning_rate)

        # Score the model
        print("Accuracy score (training): {0:.3f}".format(
            classifier.score(
                data,
                train_y)))
        print("Accuracy score (validation): {0:.3f}".format(
            classifier.score(
                test_data,
                test_y)))



    GBS_preds=classifier.predict_proba(test_data)[:,1]



    # Make Prediction
    gbs_predictions = classifier.predict(test_data)



    test_X["target"] = test_y
    test_X["GBS_Prediction"] = gbs_predictions
    test_X["GBS_preds"] = GBS_preds



    test_X.to_csv("test_results.csv")



    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import classification_report
    # Calculating the accuracy score
    acc_score = accuracy_score(test_y, gbs_predictions)
    print(f"Accuracy Score : {acc_score}")



    # Generate the confusion matrix
    cm = confusion_matrix(test_y, gbs_predictions)
    cm_df = pd.DataFrame(
        cm, index=["Actual 0", "Actual 1"],
        columns=["Predicted 0", "Predicted 1"]
    )


    from sklearn.ensemble import RandomForestClassifier
    rfc = RandomForestClassifier(n_estimators=100, max_depth=4, max_features =50)



    # Fit the model
    rfc.fit(data, train_y)


    RFC_preds=rfc.predict_proba(test_data)[:,1]



    # Make Prediction
    RFC_predictions = rfc.predict(test_data)


    test_X["target"] = test_y
    test_X["RFC_Prediction"] = RFC_predictions
    test_X["RFC_preds"] = RFC_preds



    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import accuracy_score
    from sklearn.metrics import classification_report
    # Calculating the accuracy score
    acc_score = accuracy_score(test_y, RFC_predictions)
    print(f"Accuracy Score : {acc_score}")



    # Generate the confusion matrix
    cm = confusion_matrix(test_y, RFC_predictions)
    cm_df = pd.DataFrame(
        cm, index=["Actual 0", "Actual 1"],
        columns=["Predicted 0", "Predicted 1"]
    )


    test_X.to_csv("test_results.csv")

    return(cm_df)

def eval_text(text):
    body = {}
    body["eval_title"] = "Starting Title"
    body["eval_paragraph"] = "A Paragraph to start with"
    print(body)
    return(body)  





