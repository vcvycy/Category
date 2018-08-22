import RCNNModelTest
from bottle import *
import json
model=None
@get("/")
def index():
    return static_file("index.html","web")

@post("/predict")
def predict(): 
    content=request.forms.get("content") 
    if content==None:
        content=" " 
    result=model.predict(content)
    return "%s" %(result) 
@get("/info")
def showInfo():
    return "Current Model :%s" %(model_dir)

if __name__=="__main__":
    model_dir="runs/88_keyword_not_change_category"
    #model_dir="runs/78_keyword-en-us"
    model=RCNNModelTest.ModelTest(model_dir)
    print(model.predict("china"))
    run(host="t-jianc-work",port=8080)