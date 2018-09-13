import RCNNModelTest 
import json 
from DataFilter import utils
import sys
 
if __name__=="__main__":    
    for item in utils.fileLineIter("NewsFeatures_2018_08_27_17.txt"): 
        if len(item[4])<100:
               print(item)
               input("")