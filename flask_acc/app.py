from flask import Flask,render_template
import urllib.request
import json
import pdb
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ModelTracker.html')
def tracker():
    request_url = urllib.request.urlopen('http://tiger0208.tigeranalytics.local:5000/api/2.0/mlflow/experiments/get') 
    data = json.loads(request_url.read())
    print(data)

    return render_template('ModelTracker.html',Experiment_id=data["id"])




if __name__=="__main__":
    app.run(debug=True)
