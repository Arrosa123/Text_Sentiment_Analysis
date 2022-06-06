from xml.etree.ElementTree import tostring
from flask import Flask, render_template, redirect, url_for, request, session
import json
import scraping
import Machine_Learning_spark as ml
import twitter_api_stream as tas

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

default_rules = '{"rules" : [{"value": "dog has:images", "tag": "dog pictures"},{"value": "cat has:images -grumpy", "tag": "cat pictures"}]}'

#Add empty hashtag_data to the session


## Define our routes
@app.route("/", methods=["GET", "POST"])
def index():
    #Check if there is session data for the hashtag information if not initalize the session variable
    if not session.get('hashtag_data'):
        session['hashtag_data'] = {
        "tw_title": "",
        "tw_trend_loc": "",
        "tw_trends" : []
        }
    #Get the hashtag data from the session
    hashtag_data = session.get('hashtag_data')    

    #Check if there is session data for the hashtag information
    if not session.get('rules'):
        session['rules'] = '{"rules" : [{"value": "dog has:images", "tag": "dog pictures"},{"value": "cat has:images -grumpy", "tag": "cat pictures"}]}'
    rules = session.get('rules') 

    #print(session.get('hashtag_data'))
    eval_list = []
    eval = {}
    if 'evaluate' in request.form:
        text = request.form.get("text-input")
        eval = ml.eval_text_single(text)  
        print (eval)

    if 'tweet-pull' in request.form:
        #pull the rules from the textarea input box
        rules = request.form.get("twitter-rules")
        print('rules: type: ' + rules)

        #Perform the steps needed to receive the twitter stream

        rules = json.loads(rules)
        #get the previous rules
        old_rules = tas.get_rules()

        #delete the previous rules
        delete = tas.delete_all_rules(old_rules)
        
        #set the rules to be the new rules
        set = tas.set_rules(rules["rules"])

        #Start the twitter stream with the requested rule set
        tweet_list = tas.get_stream(set) 
        
        #Send the collected twitter feed to the machine learning model
        eval_list = ml.eval_text_list(tweet_list)  
        
        #print the returned eval_list
        print(eval_list)

    if 'update-rules' in request.form:  
        new_rules = tas.create_rules(hashtag_data)
        session['rules'] = new_rules
    
    return render_template("index.html", eval=eval, eval_list = eval_list, hashtag_data = hashtag_data)

@app.route("/scrape")
def scrape():
   hashtag_data = scraping.scrape_all()   
   session['hashtag_data'] = hashtag_data
   return redirect('/', code=302)


if __name__ == "__main__":
   app.secret_key = ".."
   app.run(port=5001)



