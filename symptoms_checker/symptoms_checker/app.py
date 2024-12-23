from flask import Flask,render_template,request
import pickle

app=Flask(__name__)
with open("C:/Users/Sankrishna Goyal/PycharmProjects/symptoms_checker/model_symptom_checker.pkl",'rb') as file:
    model = pickle.load(file)
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/input",methods=['POST','GET'])
def input():
    return render_template('Symptom_Checker.html')

@app.route("/result",methods=['POST','GET'])
def result():
    lst=model.diagnose(list(request.form.values())[0]).split(":")
    return render_template("result.html",diseases=lst)

if __name__=="__main__":
    app.run(debug=True)