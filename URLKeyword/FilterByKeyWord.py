import json
import utils 
from TrieTree import Trie

#  classify url : if a url contain a keyword belong to a category; 
#  then we assume the url belong to the category
#  a url may belong to multi-category,we select the one with max priority
UsePriority = False
class KeyWord():
    def __init__(self,file):
        self.trie=Trie()
        try:
            fjson=open("URLFilter/"+file,"r")
        except:
            fjson=open(file,"r")
        # build Trie
        jsondata=json.loads(fjson.read())     
        for cat in jsondata:
            value=jsondata[cat] 
            for kw in value["keyword"]: 
                self.trie.insert(kw.lower(),cat)
        self.jsondata=jsondata
        fjson.close()
        return

    def priorityCompare(self,c1,c2):
        p1=self.getCategoryPriority(c1)
        p2=self.getCategoryPriority(c2)
        if p1>p2:
            return 1
        elif p1==p2:
            return 0
        else:
            return -1 

    def isCategoryExist(self,category):
        return category in self.jsondata

    def getJoinType(self,cat):
        try:
          return self.jsondata[cat]["join"]
        except:
          return "inner"

    def getCategoryPriority(self,category):
        try:
          return self.jsondata[category]["priority"]
        except: # category not exist
          return -1

    # if a url contain multi-keyword that belone to different category,select max priority
    def getUrlCategory(self,url):
        url=url.lower()
        category=None
        for startIdx in range(0,len(url)):
            cur_cat=self.trie.findUntilEndpoint(url.lower()[startIdx:])
            if cur_cat !=None: 
                # we assume that key word in back will be more accuracy
                if category == None or self.getCategoryPriority(cur_cat) >= self.getCategoryPriority(category):
                   category=cur_cat
        return category

def run(infile,jsonfile,outfile,max_num): 
    fin=open("Dataset/"+infile,"rb")
    fout=open("Dataset/"+outfile,"wb")
    keyword = KeyWord(jsonfile)
    cnt={}
    sum=0
    for item in utils.fileLineIter(fin): 
        url=item[0]
        category=item[1]
        subcategory=item[2]
        title=item[3]
        content=item[4] 
        # only category define in json file will be considered
        if not keyword.isCategoryExist(category):
            continue

        join=keyword.getJoinType(category)
        urlCategory = keyword.getUrlCategory(url)
        ###
        remainCurItem=False  
        if urlCategory!=None:

            if urlCategory == category or (UsePriority and (keyword.priorityCompare(urlCategory,category)>0)):
                remainCurItem=True
        elif join == "outer":
            remainCurItem=True
            urlCategory=category 

        if remainCurItem: 
            if not urlCategory in cnt:
                cnt[urlCategory]=0 
            if cnt[urlCategory] < max_num:
                if item[1]!=urlCategory:
                    item[1]=urlCategory
                    item[2]="" 
                fout.write(utils.mergeToLine(item).encode("utf-8"))
                cnt[urlCategory]+=1 
                sum+=1
    print("cnt=%s" %(cnt))
    print("sum=%s" %(sum))

if __name__ == "__main__":
    max_num_per_category = 100000
    market="en-us"
    jsonfile="%s-KeyWord.json" %(market)
    infile="FinalData_2016-07-24_2017-07-23_12_12.txt"
    #infile="FinalData_2017-07-24_2018-07-24_12_12.txt"
    outfile="%s_keyword_%s_filtered_maxnum_%s_prio%s" %(infile,market,max_num_per_category,UsePriority)
    run(infile,jsonfile,outfile,max_num_per_category)