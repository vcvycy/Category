import RCNNModelTest 
import json 
from DataFilter import utils
from Common import CategoryDataUtils
import sys

if __name__=="__main__":
    """
    urls={}
    for item in utils.fileLineIter("NewsFeatures_2018_08_27_17_Random30_Correct"):
        urls[item[0]]=item[1]
    cnt=0
    fout=open("NewsFeatures_2018_08_27_17_Random30_Origin_with_wrong_label","wb")
    for item in utils.fileLineIter("NewsFeatures_2018_08_27_17.txt"):
        if item[0] in urls: 
            str="%s %s %s\n" %(urls[item[0]],item[1],item[0])
            fout.write(str.encode("utf-8")) 
            del urls[item[0]]
    """
    for item in utils.fileLineIter("tmp.txt"):
        print(item[3]+" "+item[4])