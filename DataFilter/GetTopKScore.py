import utils
from Heap import Heap
import time 
import sys
def cmp(x,y):
    return float(x[5]) <= float(y[5])

def getTruncatedContent(content,sz):
    for i in range(len(content)):
        if content[i]==" ":
            sz-=1
        if sz<=0:
            return content[:i]
    return content 

def main(file_in,file_out,max_size_percategory,category_set,truncate=False):  
    dict_newslist={} 
    for list in utils.fileLineIter(file_in): 
        ####
        url=list[0],
        category=list[1]
        subcat=list[2]
        title=list[3] 
        ## 
        if category not in category_set:
            if category in {"rt_Canada","rt_UK","rt_NewZealand","rt_Ireland","rt_Australia","rt_India","rt_SouthAfrica"}:
                #print(category)
                category="rt_World"
                list[1]="rt_World"
                list[2]=""
            else:
                continue 
        if category not in dict_newslist:
            dict_newslist[category]=Heap(max_size_percategory,cmp)
        dict_newslist[category].insert(list)

    # write to file
    f_out=open(file_out,"wb")
    for cat in dict_newslist:
        h=dict_newslist[cat]
        print("[*] %s %d" %(cat,h.size))
        for item in h.enum():
            #item=item[:5] 
            # truncate tail and head
            """
            if truncate:
                idx=12*300
                while idx>0 and idx<len(item[4]) and item[4][idx]!=" ":
                    idx-=1
                item[4]=item[4][:idx]
                #
                idx=30
                while idx<len(item[4]) and item[4][idx]!=" ":
                    idx+=1
                item[4]=item[4][idx:]
            """
            f_out.write(utils.mergeToLine(item).encode("utf-8"))
    return

if __name__ == "__main__":
    category_set={
        "rt_Entertainment",
        "rt_Politics",
        "rt_Sports",
        "rt_US",
        "rt_Business",
        "rt_ScienceAndTechnology",
        "rt_World", 
        "rt_Health",
        "rt_LifeStyle"
        } 
    max_size_percategory=200000
    #file_in="NewsFeatures_2018_08_27_17.txt_RandomScore"
    file_in="Dataset/raw/AllDataRaw_TitleRepeat_add_score"
    #file_in="AllData_TitleRepeat_add_score"
    file_out=file_in+"_getTop_%s" %(max_size_percategory)
    main(file_in,file_out,max_size_percategory,category_set)