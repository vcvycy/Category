import re

def url_preprocess(url): 
    if url[:7]=="http://":
        url=url[7:]
    if url[:8]=="https://":
        url=url[8:]
    return url

def loadEntryList(entrylistPath):
    f=open(entrylistPath,"rb")
    list=[]
    while True:
        line=f.readline().decode("utf-8");
        if line=="":
            break;
        pair=line.split("\t")
        url=url_preprocess(pair[0].strip())
        category=pair[1].strip()
        list.append([url,category])
        print("%s %s" %(url,category))
    return list

def prefix_match(prefix_url,url):
    url=url_preprocess(url)
    return url[:len(prefix_url)]==prefix_url;

# check if data is fit in list
def check(data,list):   
    a=data.split("\t") 
    url=a[0]
    category=a[1]
    subcategory=a[2]
    title=a[3]
    content=a[4]

    for item in list:
        prefix_url=item[0]
        prefix_category=item[1]
        if prefix_match(prefix_url,url) and prefix_category!=category:
            #print("[*]don't match :%s  %s %s %s " %(prefix_category,category,prefix_url,url))
            return False
    # pass check
    return True

def filter(entrylistPath,infile,outfile):
    entrylist=loadEntryList(entrylistPath)
    fin  = open(infile,"rb")
    fout = open(outfile,"wb")
    while True:
        line_in=fin.readline() 
        if line_in == b"":
            break; 
        if check(line_in.decode("utf-8"),entrylist): 
            fout.write(line_in) 
    fin.close()
    fout.close() 

from TrieTree import *
def filter_with_trie(entrylistPath,infile,outfile):
    #init trie
    entrylist=loadEntryList(entrylistPath)
    trie=Trie()
    for item in entrylist:
        trie.insert(item[0],item[1])
    #process
    fin  = open(infile,"rb")
    fout = open(outfile,"wb")
    while True:
        line_in=fin.readline() 
        if line_in == b"":
            break; 

        a=line_in.decode("utf-8").split("\t")
        url=url_preprocess(a[0])
        category=a[1]
        subcategory=a[2]
        title=a[3]
        content=a[4]
        prefix_category=trie.getPrefixCategory(url)
        if prefix_category==None or (prefix_category==category):
            fout.write(line_in) 
    fin.close()
    fout.close() 

import time
if __name__ == "__main__": 
    entrylistPath=r"Dataset/entry_list_-1.txt"
    infile=r"Dataset/FinalData_2016-07-24_2017-07-23_12_12.txt_maxlength_500_max_per_category_100000"
    outfile=infile+"_EagleEye-1"
    t_start=time.time()
    filter_with_trie(entrylistPath,infile,outfile)
    print("Elapsed Time %s" %(int(time.time()-t_start)))