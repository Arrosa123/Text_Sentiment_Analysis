from flask import Flask, render_template, redirect, url_for, request

import Machine_Learning_spark as ml

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


## Define our routes
@app.route("/", methods=["GET", "POST"])
def index():
    if 'evaluate' in request.form:
        text = request.form.get("text-input")
        eval = ml.eval_text_single(text)  
    else:
        eval = ml.eval_text_single("This is a sample bad text.")  
     
    print (eval)
    return render_template("index.html", eval=eval)

if __name__ == "__main__":
   app.run(port=5001)   