import RCNNModelTest 
import json 
from DataFilter import utils
import sys

category_set={
        "rt_Entertainment",
        "rt_Politics",
        "rt_Sports",
        "rt_US",
        "rt_Business",
        "rt_ScienceAndTechnology",
        "rt_World", 
        "rt_Health"
        }

def getFinalCategory(probs): 
    c,p="",0.0
    prob_sum=0.0
    for cat in category_set:
        if probs[cat] > p:
            c,p=cat,probs[cat] 
        prob_sum+=probs[cat]
    probK=getKthProb(probs,4)
    if probK>1.05:
        return "rt_Unclassified",0.9
    else:
        return c,p/prob_sum;
 
def getKthProb(probs,k):
    items=[]
    for cat in category_set:
        items.append(probs[cat])
    items.sort()
    #print("%s -> %s" %(probs,items[3]))
    return items[k-1]

if __name__=="__main__":  
    #model_dir="RemoveDigit"
    #model_dir="TitleRepeat_92+"
    model_dir="WithoutQueryJoin"
    #model_dir="89.8_droup_word_0.7"
    #model_dir="92.2"
    #model_dir="Final-60000"
    #model_dir="500_0.001"
    #filetest="NewsFeatures_2018_08_27_17_Random30_Origin" 
    filetest="NewsFeatures_2018_08_27_17_Random30_Correct" 
    #filetest="NewsFeatures_2018_08_27_17.txt"
    
    result="Dataset/result_%s_%s.txt" %(filetest,model_dir)
    fout=open(result,"wb")
    ##
    model=RCNNModelTest.ModelTest("runs/"+model_dir)   
    print("model:%s" %(dir))
    _all_data=utils.GetDataList(filetest)[:400]
    all_data=[]
    for item in _all_data:
        if item[1] in category_set or item[1]=="rt_Unclassified":
            all_data.append(item)

    print("[*]read data success")
    x=[]
    for item in all_data:
        x.append(item[3]+" "+item[4]) 
    print("[*]data size:%s" %(len(x))) 
    probs=model.predict(x) 
    record={"sum":0,"diff":0}
     
    for i in range(len(all_data)):  
        item=all_data[i]
        prob= probs[i]
        url=item[0]
        category=item[1]
        title=item[3]
        content=item[4] 
        c,p=getFinalCategory(prob)
        if category not in record:
            record[category]={"sum":0,"diff":0} 
        record["sum"]+=1 
        rc=record[category]
        rc["sum"]+=1
        print("%s %s %s" %(category,c,url))
        if category!=c:
            record["diff"]+=1
            rc["diff"]+=1
            if c not in rc:
                rc[c]=[]
            rc[c].append(url)
            p=p*100
            str="%s => %s[%.1f%%] [URL]%s [Title]%s\n" %(category,c,p,url,title)
            fout.write(str.encode("utf-8"))     
    fout.write("Category different Count:\n".encode("utf-8")) 
    print("==============\n")
    for cat in record:
        if cat in category_set:
            rc=record[cat]
            #print("rc=%s" %(rc))
            str="[Real Category] %s [Accuracy] %d/%d %.2f%%\n" %(cat,rc["sum"]-rc["diff"],rc["sum"],(rc["sum"]-rc["diff"])/rc["sum"]*100)
            for cat_prediction in rc:
                if cat_prediction  in category_set: 
                    str+="  [*] Model Prediction Category %s ,count:%s\n" %(cat_prediction,len(rc[cat_prediction]))
                    #for url in rc[cat_prediction]:
                    #    print("%s %s %s" %(cat,cat_prediction,url))
            fout.write(str.encode("utf-8"))
    rate=record["diff"]/len(all_data)
    fout.write(("[*] Accuracy/Total Data :%d/%d  %.2f%%" %(len(all_data)-record["diff"],len(all_data),rate*100)).encode("utf-8"))