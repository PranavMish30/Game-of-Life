from flask import Flask,request,jsonify,render_template,redirect
from gol import gol

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/submit",methods = ["POST"])
def result():
    data = request.json
    simulationData = gol(int(data['generations']),int(data['rows']),int(data['columns']))
    return jsonify(simulationData)

if ('__main__' == __name__):
    app.run(debug=True)