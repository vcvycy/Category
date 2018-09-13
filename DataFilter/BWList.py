import json
class BWList():
    def __init__(self,file="BWList.json"):
        self.keyword = {} 
        self.all_keyword=set()
        try:
            fjson=open("DataFilter/"+file,"r")
        except:
            fjson=open(file,"r")
        #
        self.keyword=json.loads(fjson.read()) 
        for cat in self.keyword: 
            for kw in self.keyword[cat]["keyword"]:
              self.all_keyword.add(kw) 
        return 
     
    def isInWhiteList(self,url,category):
        url=url.lower()
        try:
            l = self.keyword[category]["keyword"]
        except:
            return False 
        for item in l:
            if url.find(item)!=-1:
                return True
        return False 

    def isInAllKeyWord(self,url):
        url=url.lower()
        for kw in self.all_keyword:
            if url.find(kw)!=-1:
                return True
        return False

if __name__== "__main__":
    bwList=BWList("BWList.json")
    print(bwList.isInWhiteList("/SPortss","rt_Sports"))
    
    print(bwList.isInAllKeyWord("/us"))