from Common import Utils
from Common import ArticleFilter
from Common import CategoryDataUtils
import random 
import time
## 
class MYData: 
    def __init__(self,datafile,
                 minSizePerCategory,
                 max_article_length=400,
                 min_frequence=5,
                 training_share=0.9,
                 droup_out=1.0             # not implement now

                 ): 
        self.text_data={}  # category ->article word list
        self.total_size=0
        self.initTextData(datafile,minSizePerCategory)  
        self.data,self.vocabSize,self.vocabproc=CategoryDataUtils.category_dict2vec_vocabular_processor(self.text_data,
                                                                                    max_article_length=400,
                                                                                    min_freq=min_frequence,
                                                                                    ) 

        # split self.data into training/testing data
        self.test_data={}  #{"world":["article","artile"...],...}
        self.training_share=training_share;
        self.splitIntoTrainingAndTestData()  #
        # cat 2 idx (sorted)
        self.cat2idx={}
        cats=[]
        for cat in self.text_data:
            cats.append(cat)
        cats.sort()
        for i in range(len(cats)):
            self.cat2idx[cats[i]]=i 
        # one hot
        self.oneHot=[]
        for i in range(self.getClasses()):
            y=[0 for _ in range(self.getClasses())]
            y[i]=1
            self.oneHot.append(y) 

        self.showDetail() 
        return  

    def saveCategory2Index(self,path):
        a=["" for _ in range(self.getClasses())]
        for key in self.cat2idx:
            a[self.cat2idx[key]]=key
        f=open(path,"w")
        for i in range(self.getClasses()):
            f.write("%d:%s\n" %(i,a[i]))
        return

    def showDetail(self):
        print("[*]Data Detail:total size:%s  training_share=%s" %(self.getDataSize(),self.training_share))
        print("[*]Vocabulary Size :%s " %(self.vocabSize)) 
        for cat in self.data:
            print("  [*]Class %d: %s num:%s + %s" %(self.cat2idx[cat],cat,len(self.data[cat]),len(self.test_data[cat])))  
        #print(self.data["rt_World"][0])
        return 

    def splitIntoTrainingAndTestData(self): 
        for cat in self.data:
            split_idx=int(len(self.data[cat])*self.training_share)
            self.test_data[cat]=self.data[cat][split_idx:]
            self.data[cat]=self.data[cat][:split_idx]
        return 

    #read text data from datafile to self.data 
    def initTextData(self,datafile,minSizePerCategory):
        #
        print("[*]init Text Data")
        t_start=time.time()
        self.text_data={} 
        list = CategoryDataUtils.GetDataList(datafile) 
        for category,url,title,content,_ in list: 
            if not (category in self.text_data):
                self.text_data[category]=[] 
            #self.text_data[category].append(ArticleFilter.considerHost(url,title,content))
            self.text_data[category].append(ArticleFilter.regular(url,title,content))
        #
        tmp={}
        for cat in self.text_data:
            if len(self.text_data[cat]) >=minSizePerCategory:
                tmp[cat]=self.text_data[cat]
                self.total_size+=len(tmp[cat])
            else:
                print("[!] Category %s ; sample size: %d removed" %(cat,len(self.text_data[cat])))
        self.text_data=tmp
        return 

    # get total size
    def getDataSize(self):
        return self.total_size

    def getClasses(self): 
        return len(self.data) 

    def nextBatch(self,batchSize):
        batch=[[],[]]
        size_per_category=int(batchSize/self.getClasses())
        if size_per_category * self.getClasses() !=batchSize:
            print("[!] New Batch Size:%s " %(size_per_category * self.getClasses()))

        while size_per_category>0:
            size_per_category-=1
            for cat in self.data: 
                catIdx=random.randint(0,len(self.data[cat])-1)
                batch[0].append(self.data[cat][catIdx])
                #batch[1].append(CategoryDataUtils.toOneHot(self.cat2idx[cat],self.getClasses()))
                batch[1].append(self.oneHot[self.cat2idx[cat]])
                
        return batch 

    def getTestData(self):
        batch=[[],[]]
        for cat in self.test_data:
            catIdx=self.cat2idx[cat]
            for i in range(len(self.test_data[cat])):
              batch[0].append(self.test_data[cat][i])
              batch[1].append(self.oneHot[catIdx])
        return batch
     
if __name__=="__main__":
    #mydata=MYData("0708-0728-0-3.tsv")
    t_start=time.time()
    #file="Dataset/Data-9000"
    file="Dataset/FinalData_2017-07-24_2018-07-24_12_12.txt_maxlength_500_max_per_category_100000_EagleEye-1"
    mydata=MYData(file,
                minSizePerCategory=10,
                max_article_length=400,
                min_frequence=10,
                training_share= 0.9,
                droup_out=0.7          # will random remove word from article
                )  
    print("[*]Elapsed Time: %s" %(time.time()-t_start))