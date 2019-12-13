from flask import Flask,render_template, jsonify
import urllib.request
import json
import pdb
import datetime

app=Flask(__name__)

def get_metrics(data_list):
    final_string = ""
    for ele in data_list:
        final_string = final_string + "{} : {}".format(ele['key'],ele['value']) + "<br>"
    return final_string

def get_souce_name(tag_list):
    for ele in tag_list:
        if ele['key'] == "mlflow.source.name":
            return ele['value']

def get_run_name(tag_list):
    for ele in tag_list:
        if ele['key'] == "mlflow.runName":
            return ele['value']
def get_ml_name(tag_list):
    for ele in tag_list:
        if ele['key'] == "ml_algorithm":
            return ele['value']
def get_params(data_list):
    final_string = ""
    for ele in data_list:
        final_string = final_string + "{} : {}".format(ele['key'],ele['value']) + "<br>"
    return final_string

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/modeltracking')
def tracker():
    
    return render_template('modeltracking.html')
@app.route("/get_response")
def json_data():
    with open("response.json") as json_file:
        json_data = json.load(json_file)
    # pdb.set_trace()
    data = []
    all_runs_data = json_data['runs']
    for run_data in all_runs_data:
        record = {}
        record['experiment_id'] = run_data['info']['experiment_id']
        record['user_id'] = run_data['info']['user_id']
        record['status'] = run_data['info']['status']
        # pdb.set_trace()
        record['date'] = str(datetime.datetime.fromtimestamp(int(run_data['info']['start_time'])/1000))
        record['source'] = run_data['data']['tags'][2]['value']
        record['metrics'] = get_metrics(run_data['data']['metrics'])
        record['runname'] = get_run_name(run_data['data']['tags'])
        record['ml_algorithms'] = get_ml_name(run_data['data']['tags'])
        record['params']=get_params(run_data["data"]['params'])

        data.append(record)

    final_data = {}
    final_data["data"] = data
    final_data["header"] = [{"title":"Check Box",

                             "data": "<input type='checkbox'>"},
                        
                     {"title":"Run Name",
                             "data": "runname"
                        },
                        {"title":"Date",
                             "data": "date"
                        },
                        {"title":"Algorithms Used",
                            "data": "ml_algorithms"
                        },
                        {"title":"User",
                            "data": "user_id"
                        },
                        {"title":"Status",
                            "data": "status"
                        },
                        {"title":"Source",
                            "data": "source"
                        },
                        {"title":"Parameters",
                            "data": "params"
                        },
                        {"title":"Metrics",
                            "data": "metrics"
                        }
                    ]
    return jsonify(final_data)
#     request_url = urllib.request.urlopen('http://tiger0208.tigeranalytics.local:5000/api/2.0/mlflow/experiments/get') 
#     data = json.loads(request_url.read())
#     print(data)

   




if __name__=="__main__":
    app.run(debug=True)
