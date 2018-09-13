from Trie import Trie
import utils
import sys
from BWList import BWList
import time
import random
if __name__ == "__main__":
    files_in=["Dataset/raw/WithoutQueryJoin_en_2017-08-29_2018-08-28_17_17.txt",
              "Dataset/raw/WithoutQueryJoin_en_2017-08-29_2018-08-28_14_14.txt"]
    file_out="Dataset/raw/AllData"
    #
    fout = open(file_out,"wb")   
    for list in utils.filesLineIter(files_in): 
        fout.write(utils.mergeToLine(list).encode("utf-8"))