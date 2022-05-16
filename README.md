# Text_Sentiment_Analysis

## Purpose and reason to select this topic:
The exponential growth of social media has brought with it an increasing propagation of hate speech and hate based propaganda. Hate speech is commonly defined as any communication that disparages a person or a group on the basis of some characteristics such as race, color, ethnicity, gender, sexual orientation, nationality, religion. Online hate diffusion has now developed into a serious problem and this has led to a number of international initiatives being proposed, aimed at qualifying the problem and developing effective counter-measures. 
  The aim of this project is to divide a message or text in to positive or negative and that can help the social media sites to block the message. This kind of messages have such deep and negative effect on people. We are also trying to show those effects through visual representation of the date we will gather (in process) - we sill show them in tables and graphs to make it easy to understand for everyone.

## Questions we hope to answer with this data:

# Q.1: Why it is important to detect speech sentiments?
In social media, people can express their opinions but sometimes it express their hatred, dislike, other negative emotions- it can hurt people in many ways. They might have felt that way due to their past experiences but someone's personal experience can not define one whole group of people. We have good and bad people in all races, countries, religions - it is not fair to blame the whole group for that. So if we can catch an negative text early enough to block it before other people read it.

# Q:2: How the negative speech affect people?
We are currently gathering data to show the effects of negative texts or messages on people. There is a direct correlation between them as we all know and a strong impact so we are trying to show the same through data visualization with graphs and tables.

## Data sources: 
- [Sentiment140 dataset with 1.6 million tweets](http://help.sentiment140.com/for-students)
  - [20k sample dataset (10k pos/10k neg)](./Resources/sentiment_analysis_10k.csv)

## Machine Learning Model
Using pyspark to create a data pipeline for NLP.  
- I import a 20k sample of the dataset from an AWS S3 bucket
- tokenized the data
- removed the stopwords
- use tf/idf to hash and vectorize the data
- use Naive Bayes classifier to predict a positive or negative sentiment
- Finally exporting the data to AWS RDS PostgreSQL instance.
- I exported the test results data from the database to a csv file and checked it into github. 


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


## Team members: 
  * Arrosa Qayyum
  * Ilan Prudhomme
  * Nayan Barhate
  * Kiran Dave
