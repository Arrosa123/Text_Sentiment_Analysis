# Text_Sentiment_Analysis
![image](https://github.com/Arrosa123/Text_Sentiment_Analysis/blob/main/images1.png)

## Purpose and reason to select this topic:

  The aim of this project is to categorize a sentence or a tweet to positive or negative with our knowledge of Machine Learning, Python, HTML, Flask, Database and Web Scraping. We have a webpage where a user can input a sentence and our code decides whether the given sentence is positive or negative with it's probability score. Anything over probability of 0.5 is catagorized as positive. We developed a tool which can be used in many different ways. For example, on websites like Facebook, Twitter, etc. or even at workplace connection pages, we can use this tool to stop people from posting negative comments with hatred or discriminationg statements.

## Questions we hope to answer with this data:

# Q:1: Why it is important to detect speech sentiments?
In social media, people can experess their opinions but sometimes it expresses their hatred, dislikeness towards somethng, other negative emotions. This can hurt people in many ways. They might have felt that way due to their past experiences but someone's personal experience can not define one whole group of people. We have good and bad people in all races, countries, religions, so it is not fair to blame the whole group for that. So if we can catch an negative text early enough to block it before other people read it, it would be very helpful.

# Q:2: How the negative speech affect people?
We are currently gathering data to show the effects of negative texts or messages on people. There is a direct correlation between them as we all know that it causes a  strong impact on people, so we are trying to show the same through data visualization with graphs and tables.

## Presentation: 
[Click here to go to our Google Slides Presentation](https://docs.google.com/presentation/d/1JQpK-gHvPBrHtgzteNTrwzFp4QcuEgPoajs-kB3tmf4/edit?usp=sharing)

## Data sources: 
- [Sentiment140 dataset with 1.6 million tweets](http://help.sentiment140.com/for-students)
- [20k sample dataset (10k pos/10k neg)](./Resources/sentiment_analysis_10k.csv)

## Machine Learning Model
Using PySpark to create a data pipeline for NLP.  
- I imported a 20k sample of the dataset from an AWS S3 bucket
- tokenized the data
- removed the stopwords
- used tf/idf to hash and vectorize the data
- used Naive Bayes classifier to predict a positive or negative sentiment
- I finally exported the data to AWS RDS PostgreSQL instance.
- I then exported the test results data from the database to a csv file and checked it into GitHub. 

## languages and technologies used during this project:
* Python
* PostgreSQL 
* Machine learning
  * pyspark.ml.feature
    * Tokenizer, StopWordsRemover, HashingTF, IDF, StringIndexer, VectorAssembler
  * pyspark.ml.Pipeline
  * pyspark.ml.classification.NaiveBayes
  * pyspark.ml.evaluation.BinaryClassificationEvaluator
* VS code
* Jupyter Notebook
* Bootstrap
* JavaScript/HTML
* Plotly
* Git
* AWS



## Team members: 
  * Arrosa Qayyum: 
  [linkedin.com/in/arrosa-qayyum-824b02225](linkedin.com/in/arrosa-qayyum-824b02225)
  * Ilan Prudhomme: [linkedin.com/in/iprudhomme](linkedin.com/in/iprudhomme)
  * Nayan Barhate: [linkedin.com/in/nayan-barhate-83a65a187](linkedin.com/in/nayan-barhate-83a65a187)
  * Kiran Dave: [linkedin.com/in/kiran-dave-42b716136](linkedin.com/in/kiran-dave-42b716136)
