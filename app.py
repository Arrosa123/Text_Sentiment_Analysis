from xml.etree.ElementTree import tostring
from flask import Flask, render_template, redirect, url_for, request
import json

import Machine_Learning_spark as ml
import twitter_api_stream as tas

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

default_rules = '{"rules" : [{"value": "dog has:images", "tag": "dog pictures"},{"value": "cat has:images -grumpy", "tag": "cat pictures"}]}'

## Define our routes
@app.route("/", methods=["GET", "POST"])
def index():
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
    
    return render_template("index.html", eval=eval, eval_list = eval_list)

if __name__ == "__main__":
   app.run(port=5001)



