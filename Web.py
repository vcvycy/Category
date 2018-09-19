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
    #model_dir="runs/88_keyword_not_change_category"
    #model_dir="runs/78_keyword-en-us"
    #model_dir="runs/len_500_will_deleted"
    #model_dir="runs/500_0.001"
    #model_dir="runs/Final-60000"
    #model_dir="runs/91.8"
    #model_dir="runs/88.5_prefix_filter"
    #model_dir="runs/92.2"
    #model_dir="runs/TitleRepeat_92+"
    #model_dir="runs/RemoveDigit"
    model_dir="runs/NewCleanText"
    
    model=RCNNModelTest.ModelTest(model_dir)
    print(model_dir)
    run(host="t-jianc-work",port=8081)