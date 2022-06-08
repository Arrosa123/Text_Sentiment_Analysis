from xml.etree.ElementTree import tostring
from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory
import json
import scraping
import Machine_Learning_spark as ml
import twitter_api_stream as tas

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

## Define our routes
@app.route("/", methods=["GET", "POST"])
def index():
   # Initialize variables that will be assigned later based on user requests
    eval_list = []
    eval = {}
    top_10 = []
    bottom_10 = []
        
    #Check if there is session data for the hashtag information if not initalize the session variable
    if not session.get('hashtag_data'):
        session['hashtag_data'] = {
        "tw_title": "",
        "tw_trend_loc": "",
        "tw_trends" : []
        }
    #Get the hashtag data from the session
    hashtag_data = session.get('hashtag_data')    
    
    if not session.get('top_10'):
        session['top_10'] = {}
    #Get the top_10 from the session
    top_10 = session.get('top_10')     

    if not session.get('bottom_10'):
        session['bottom_10'] = {}
    #Get the top_10 from the session
    bottom_10 = session.get('bottom_10')  

    #Check if there is session data for the hashtag information
    if not session.get('rules'):
        session['rules'] = '{"rules" : [{"value": "dog has:images", "tag": "dog pictures"},{"value": "cat has:images -grumpy", "tag": "cat pictures"}]}'
    rules = session.get('rules') 

    # if the submit button for evaluate is pressed
    if 'evaluate' in request.form:
        text = request.form.get("text-input")
        eval = ml.eval_text_single(text)  
        print (eval)

    # If the submit button for processing the twitter API feed
    if 'tweet-pull' in request.form:
        #pull the rules from the textarea input box
        rules = request.form.get("twitter-rules")

        #pull the number of Tweets to request from the Twitter API
        countOfTweets = request.form.get("quantity")
        print(f'Count of Tweets: {str(countOfTweets)}')
        if countOfTweets is None:
            countOfTweets = 10

        #Perform the steps needed to receive the twitter stream 

        rules = json.loads(rules)
        #get the previous rules
        old_rules = tas.get_rules()

        #delete the previous rules
        delete = tas.delete_all_rules(old_rules)
        
        #set the rules to be the new rules
        set = tas.set_rules(rules["rules"])

        #Start the twitter stream with the requested rule set
        tweet_list = tas.get_stream(countOfTweets) 
        
        #Send the collected twitter feed to the machine learning model
        eval_list, top_10, bottom_10 = ml.eval_text_list(tweet_list)  
        
        #Save the full list to a json file. 
        with open('static/resources/evaluated_tweets.json', 'w') as fp:
            json.dump(eval_list, fp)

        session['eval_list'] = json.dumps(eval_list)  
        #print the returned eval_list
        print(session['eval_list'])

    # If the button to update the rules based on the trending hashtags is pressed
    if 'update-rules' in request.form:  
        new_rules = tas.create_rules(hashtag_data)
        session['rules'] = new_rules

    session['top_10'] = top_10
    session['bottom_10'] = bottom_10


    
    return render_template("index.html", eval=eval, hashtag_data = hashtag_data, top_10 = top_10, bottom_10 = bottom_10)

# add the resources folder to the path so that data will be available to javascript
@app.route("/<path:path>")
def static_dir(path):
    return send_from_directory("static", path)

# The scrape route performs a lookup on a website for the current trending Twitter hashtags and returns them for our use.
@app.route("/scrape")
def scrape():
   hashtag_data = scraping.scrape_all()   
   session['hashtag_data'] = hashtag_data
   return redirect('/', code=302)

# The scrape route performs a lookup on a website for the current trending Twitter hashtags and returns them for our use.
@app.route("/plot")
def plot():
    #Check if there is session data for the hashtag information
    if not session.get('eval_list'):
        session['eval_list'] = {}
    eval_list = session.get('eval_list') 
    print('Rendering plots.html')
    return render_template("plots.html", eval_list = eval_list)

# The scrape route performs a lookup on a website for the current trending Twitter hashtags and returns them for our use.
@app.route("/reset")
def reset():
   for key in list(session.keys()):
       session.pop(key)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.secret_key = ".."
   app.run(port=5001)



