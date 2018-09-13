import sys

CHARACTER_SIZE=127
def char2idx(ch): 
    if ord(ch)>=48 and ord(ch)<=57:
        ch='0'
    return ord(ch)

def idx2char(idx): 
    return chr(idx)

cat2idx={}
idx2cat=[]
catSize=0

def prefix_strip(prefix):
    while len(prefix)>0 and (prefix[-1]=='/' or prefix[-1]=='0'):
        prefix=prefix[:-1]
    return prefix+'/'

def url_strip(url): 
    # remove get parameter
    for i in range(len(url)):
        if url[i]=="?":
            url=url[:i]
            break 
    # 
    idx=len(url)-1
    while idx>0:
        if url[idx]=='/':
            return url[:idx+1]
        idx-=1
    return url

#check if current node belong to some category based on the conditions.
#return None or Category Name
global_count=0
global_removed={}
def check(sum,catCnt,min_occur,threshold): 
    global global_count
    global global_removed
    if min_occur >sum:
        return None,0
    ret=None
    share=0
    for cat in catCnt:
        if catCnt[cat] >= sum*threshold: 
            global_count+=catCnt[cat] 
            ret=cat
            share=catCnt[cat]/sum
            break
    if ret!=None:
        for cat in catCnt:
            if catCnt[cat] < sum*threshold:
                catname=idx2cat[cat]
                if catname not in global_removed:
                    global_removed[catname]=0
                global_removed[catname] += catCnt[cat] 
    return ret,share

class Node:
    def __init__(self):
        self.next=[None for i in range(CHARACTER_SIZE)]
        self.msg={} 
        self.sum=0
        return

    def go(self,ch,createIfNotExist=False): 
        idx=char2idx(ch)
        if createIfNotExist and self.next[idx] == None:
            self.next[idx]=Node() 
        return self.next[idx] 

    # if exist prefix satisfy our condition,return True,else return False
    def analyse(self,prefix,fout,min_occur,threshold):
        exist_more_accuracy_split=False
        for i in range(CHARACTER_SIZE):
            if self.next[i]!=None:
                if self.next[i].analyse(prefix+idx2char(i),fout,min_occur,threshold):
                    exist_more_accuracy_split=True
        ###
        if exist_more_accuracy_split:
            return True
        # check current prefix 
        belongtocategory=None 
        if len(prefix)>0 and prefix[-1]=='/':
        #analyse current prefix 
            belongtocategory,share = check(self.sum,self.msg,min_occur,threshold)
        #
        if belongtocategory==None:
            return False
        else:
            #if belongtocategory not in dict_cat_prefix:
            #    dict_cat_prefix[belongtocategory]=[]
            #dict_cat_prefix[belongtocategory].append((prefix_strip(prefix),self.msg))
            global idx2cat
            fout.write("%s\t%.2f\t%s\t" %(idx2cat[belongtocategory],share,prefix_strip(prefix)))
            for idx in self.msg:
                fout.write("%s:%s " %(idx2cat[idx],self.msg[idx]))
            fout.write("\n")
            return True

class URLTrie:  
    def __init__(self,min_occur=10,threshold=0.9):
        self.root=Node()
        self.min_occur=min_occur
        self.threshold=threshold
        self.url_count=0
        return 

    def insert(self,str,category): 
        self.url_count+=1
        try:
            cur_node=self.root 
            for ch in str:
                cur_node = cur_node.go(ch,True)
                # count in occurence of '/'
                if ch=='/':
                    if category not in cur_node.msg:
                        cur_node.msg[category]=1
                    else:
                        cur_node.msg[category]+=1 
                    cur_node.sum+=1
        except: # non-ascii code
            return
        return 
    
    #
    def analyse(self,fout): 
        self.root.analyse("",fout,self.min_occur,self.threshold)
        global global_count
        global global_removed 
        sum=0
        for cat in global_removed:
            sum+=global_removed[cat]
        fout.write("Example:%s/%s sum:%s removed: %s " %(global_count,self.url_count,sum,global_removed))
        return  

import utils
import time
def main(file,outfile,min_freq,threshold,startLine,endLine):
     trie=URLTrie(min_freq,threshold) 
     global cat2idx
     global catSize
     global idx2cat
     cat2idx={}
     catSize=0
      
     for list in utils.fileLineIter(file,startLine,endLine):
         url = url_strip(list[0])  #default url=list[0]
         category = list[1]        #[default] category=list[1]
         if category not in cat2idx:
             cat2idx[category]=catSize
             idx2cat.append(category)
             catSize+=1
         trie.insert(url,cat2idx[category])  

     #print("[*]Insert")
     fout=open(outfile,"w")
     trie.analyse(fout) 

if __name__ == "__main__": 
     #print(url_strip("http://bigozine2.com/roio/?p=3909"))
     #sys.exit(0) 
     t_start=time.time()
     min_freq=10
     threshold=0.7
     startLine=0
     endLine=2000000
     #infile="Dataset/FinalData_2017-07-24_2018-07-24_12_12.txt_only_url_catagory"
     #infile="Dataset/FinalData_2016-07-24_2017-07-23_12_12.txt"
     infile="Dataset/Data-9000" 
     outfile=infile+"_url_prefix_distribution_%s_%s_%s_%s" %(min_freq,threshold,startLine,endLine)
     main(infile,outfile,min_freq,threshold,startLine,endLine)
     print("[*]Time Elapsed:%s" %(time.time()-t_start))