import sys
import utils
import time
def removeLastZero(prefix):
    while len(prefix)>0 and (prefix[-1]=='/' or prefix[-1]=='0'):
        prefix=prefix[:-1]
    return prefix+'/'

def url_process(_url):  
    _url=_url.lower()
    """
    if url[:8]=="https://":
        url=url[8:]
    if url[:7]=="http://":
        url=url[7:]
    """
    url=""
    for i in range(0,len(_url)):
        asc=ord(_url[i])
        if asc>=ord('0') and asc<=ord('9'):
            url+="0"
        elif asc<128:
            url+=_url[i]
        else:
            break

    # remove get parameter
    for i in range(len(url)):
        if url[i]=="?":
            url=url[:i]
            break 
    # 
    idx=len(url)-1
    while idx>0:
        if url[idx]=='/':
            url=url[:idx]
            break
        idx-=1
    url_split=url.split("/")
    return url_split

class Node: 
    def __init__(self):
        self.next={}
        self.count={}
        self.sum=0
        return

    def go(self,edgeVal,creatIfNotExist=False):
        if creatIfNotExist and edgeVal not in self.next:
            self.next[edgeVal] = Node()
        if edgeVal not in self.next:
            return None
        return self.next[edgeVal]

    def inc_count(self,catIdx): 
        self.sum+=1
        if catIdx not in self.count:
            self.count[catIdx]=0
        self.count[catIdx]+=1
        return

class PrefixTree:
    # each category has a idx(to reduce memory usage)
    catNum=0
    catIdx={}
    idxCat={}
    # each word has a idx(to reduce memory usage)
    wordNum=0
    wordIdx={}
    idxWord={}
    #
    reservedSumMaxCat=0
    reservedSum=0
    reservedEachCat={}
    def __init__(self,minFreq,threshold):
        self.minFreq=minFreq
        self.threshold=threshold
        self.root=Node()
        return
    def getTotalNum(self):
        return self.root.sum

    def addReservedNum(self,node,maxCatNum):
        self.reservedSumMaxCat+=maxCatNum
        self.reservedSum+=node.sum 
        for catIdx in node.count:
            category=self.idxCat[catIdx]
            if category not in self.reservedEachCat:
                self.reservedEachCat[category]=0
            self.reservedEachCat[category]+=node.count[catIdx]
        return

    def getWordIdx(self,word):
        if word not in self.wordIdx:
            self.wordNum+=1
            self.wordIdx[word]=self.wordNum
            self.idxWord[self.wordNum]=word
        return self.wordIdx[word]

    def getCatIdx(self,category):
        if category not in self.catIdx:
            self.catNum+=1
            self.catIdx[category]=self.catNum
            self.idxCat[self.catNum]=category
        return self.catIdx[category]

    def insert(self,url,category):
        url_split=url_process(url)
        catIdx=self.getCatIdx(category)
        self.root.inc_count(catIdx)
        #
        curNode=self.root; 
        for part in url_split: 
            partIdx=self.getWordIdx(part) 
            curNode=curNode.go(partIdx,True)
            curNode.inc_count(catIdx)
        return

    def writeListToFile(self,f,curNode=None,prefix=""):  
        if curNode==None:
            curNode=self.root
        findPrefixInSon=False
        for wordIdx in curNode.next:
            nxtNode=curNode.next[wordIdx]
            nxtPrefix=prefix+self.idxWord[wordIdx]+"/"
            if self.writeListToFile(f,nxtNode,nxtPrefix):
                findPrefixInSon = True

        if not findPrefixInSon:
            if curNode.sum < self.minFreq: 
                return False
            maxCatIdx=""
            maxCatNum=0
            for catIdx in curNode.count:
                if curNode.count[catIdx]>maxCatNum:
                    maxCatNum=curNode.count[catIdx]
                    maxCatIdx=catIdx
            share=maxCatNum/curNode.sum
            if share < self.threshold:  
                return False
            self.addReservedNum(curNode,maxCatNum)
            f.write("%s\t%.2f\t%s\t" %(self.idxCat[maxCatIdx],share,removeLastZero(prefix)))
            for catIdx in curNode.count: 
                f.write("%s:%s " %(self.idxCat[catIdx],curNode.count[catIdx]))
            f.write("\n")
        ###########
        return True

def main(file,outfile,min_freq,threshold):  
     prefixTree=PrefixTree(min_freq,threshold)
     for list in utils.filesLineIter(file):
         url=list[0]
         category=list[1]
         if list[2]!="":
            category+="/"+list[2]
         prefixTree.insert(url,category) 
     print(prefixTree.root.sum)
     f=open(outfile,"w")
     prefixTree.writeListToFile(f)
     f.write("Total:%s  %s+%s/%s %s" %(prefixTree.getTotalNum(),prefixTree.reservedSumMaxCat, 
                                     prefixTree.reservedSum-prefixTree.reservedSumMaxCat,
                                     prefixTree.reservedSum,prefixTree.reservedEachCat))
     return

if __name__ == "__main__":  
     # Get Prefix List
     t_start=time.time()
     min_freq=10
     threshold=0.7 
     #infile="Dataset/Data-9000"
     infile="Dataset/raw/AllDataRaw_TitleRepeat" 
     outfile=infile+"_SubCategory_PrefixList_%s_%s" %(min_freq,threshold) 
     main(infile,outfile,min_freq,threshold)
     print("[*]Time Elapsed:%s" %(time.time()-t_start))