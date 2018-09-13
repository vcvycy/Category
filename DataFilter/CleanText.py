import utils
from Heap import Heap
import time 
import re
import sys  

def clean_str(string):
    """
    Tokenization/string cleaning for all datasets except for SST.
    Original taken from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    """
    string = re.sub(r"[^A-Za-z0-9(),!?\'\`]", " ", string)
    string = re.sub(r"\'s", " \'s", string)
    string = re.sub(r"\'ve", " \'ve", string)
    string = re.sub(r"n\'t", " n\'t", string)
    string = re.sub(r"\'re", " \'re", string)
    string = re.sub(r"\'d", " \'d", string)
    string = re.sub(r"\'ll", " \'ll", string)
    string = re.sub(r",", " , ", string)
    string = re.sub(r"!", " ! ", string)
    string = re.sub(r"\(", " \( ", string)
    string = re.sub(r"\)", " \) ", string)
    string = re.sub(r"\?", " \? ", string)
    string = re.sub(r"\s{2,}", " ", string)
    ##
    string = re.sub(r" [^A-Za-z?!;,.]+ "," 0 "," "+string+" ")
    return string.strip().lower()

def main(file_in,file_out):   
    fout=open(file_out,"wb")
    for item in utils.fileLineIter(file_in):
        title=clean_str(item[3])
        body=clean_str(item[4])  
        item[3]=title
        item[4]=body
        fout.write(utils.mergeToLine(item).encode("utf-8"))
    return

if __name__ == "__main__": 
    #file_in="Dataset/AllData_TitleRepeat_add_score_getTop_200000" 
    file_in="Dataset/Data-9000"
    file_out=file_in+"_CleanText"
    main(file_in,file_out)