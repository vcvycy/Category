from Trie import Trie
import utils
import sys
from BWList import BWList
import time
import random

def getScore(msg,category):
    try:
        x=msg[1][category]
        return x*x/msg[0]
    except:
        return 0

def buildTrie(files):
    trie=Trie()
    for list in utils.filesLineIter(files): 
        if len(list)!=4:
            continue
        url=list[2]
        catNum={}
        sum=0 
        for item in list[3].split(" "):
            kv=item.split(":")
            kv[1]=int(kv[1])
            catNum[kv[0]]=kv[1]
            sum+=kv[1] 
        trie.insert_merge(url,[sum,catNum]) 
    return trie 

def main(prefix_files,news_files_in,news_file_out): 
    if news_file_out[:8]!="Dataset/":
        news_file_out="Dataset/"+news_file_out
    news_out = open(news_file_out,"wb")  
    # (1) Black/White List
    bwList=BWList() 
    delCnt={}
    print("[*]load black/white list success")
    # (2) Preifix tree
    trie=buildTrie(prefix_files)
    print("[*]load prefix files success")
    # run
    cnt=0 
    for list in utils.fileLineIter(news_files_in): 
        url=list[0]
        category=list[1]
        subcat=list[2]
        title=list[3]
        content=list[4]
        if category=="rt_Unclassified":
            continue
        #
        removed =None
        # black list/ min content size
        score = trie.getScore(url,category)
        if  bwList.isInWhiteList(url,category):
            score *= 2
        #elif bwList.isInAllKeyWord(url):
        #    score /= 2  
        # if content is too short ,will be punished
        c_len=len(content)
        if c_len < 600:
            score*=c_len/600; 
        # same score will be choose randomly
        score+=random.randint(10000,99999)/1000000000
        list.append(score)
        #list.append(random.randint(0,10000000))
        news_out.write(utils.mergeToLine(list).encode("utf-8")) 
    return

if __name__ == "__main__":
    #add score and remove unclassified 
    #prefix_files=["Dataset/raw/AllDataRaw_TitleRepeat_PrefixListByDict_10_0.7"]
    prefix_files=["Dataset/AllDataPlus_TitleRepeat_PrefixListByDict_10_0.5"]
    news_files_in="Dataset/AllDataPlus_TitleRepeat" 
    #news_files_in = "Dataset/raw/AllDataRaw_TitleRepeat"
    news_file_out="%s_add_score" %(news_files_in)
    main(prefix_files,news_files_in,news_file_out)