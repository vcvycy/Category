import re
import sys
from Common import Utils 
import tensorflow as tf
import time
import numpy as np

def shuffle_list(list):
    n=len(list)
    for i in range(n):
        k=random.randint(0,i)
        list[i],list[k]=list[k],list[i]

def showDictData(dict_data):
    print("[*]Data Detail:total categories:%s " %(dict_data))
    idx=0
    for cat in dict_data:
        print("  [*]Class %d: %s num:%s" %(idx,cat,len(dict_data[cat])))
        idx+=1
    return 

#   line = url [TAB] category [TAB] subcategory [TAB] title [TAB] content [\r\n]
def parseLine(line): 
    pos=[m.start() for m in re.finditer("\t",line)]
    if len(pos)<4:
        Utils.error("len(pos)<4")
    url=line[0:pos[0]]
    category=line[pos[0]+1:pos[1]]
    subcategory=line[pos[1]+1:pos[2]]
    title=line[pos[2]+1:pos[3]]
    if len(pos)>4:
        content=line[pos[3]+1:pos[4]]
    else:
        content=line[pos[3]+1:]
    #
    url=url.strip()
    category=category.strip()
    title=title.strip()
    content=content.strip()
    subcategory=subcategory.strip()
    return category,url,title,content,subcategory

# get all category type from data list
def getCategoryListAndCnt(data):
    categoryList=[]
    categoryCnt=[]
    for item in data:
        if len(categoryList)==0 or item[0]!=categoryList[-1]:
            categoryList.append(item[0])
            categoryCnt.append(1)
        else:
            categoryCnt[-1]+=1
    return categoryList,categoryCnt

#read data from filename
def GetDataList(filename):
    if type(filename)==type([]):
      return GetDataListFromMultiFile(filename)
    t_start=time.time()
    list=[]
    try:
        f=open(filename,"rb")
    except: 
        f=open("Dataset/"+filename,"rb")
    while True:
        line=f.readline().decode("utf-8")
        if line!="":
            list.append(parseLine(line))
        else:
            break
    print("  [*]Get Data List %s Time: %s" %(filename,int(time.time()-t_start)))
    return list
#read data from multi file
def GetDataListFromMultiFile(files):
    list=[]
    for filename in files:
        list+=GetDataList(filename)
    return list
#
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
    return string.strip().lower()

def textListPreprocess(all_text):
    return [clean_str(sent) for sent in all_text]

def toOneHot(idx,classes):
    y=[0 for i in range(classes)]
    y[idx]=1
    return y

# return vocab_size,category->
def category_dict2vec_vocabular_processor(category_dict,max_article_length,min_freq,saveVocabTo=None): 
    print("  [*] vocabulary processor")
    t_start=time.time()
    text_vocab_processor = tf.contrib.learn.preprocessing.VocabularyProcessor(max_article_length,min_frequency=min_freq)  
    all_text=[] 
    for cat in category_dict: 
        all_text+=category_dict[cat]
    all_text = [clean_str(sent) for sent in all_text]
    print("  [*] clearn str success %s" %(int(time.time()-t_start)))
    text2digit = np.array(list(text_vocab_processor.fit_transform(all_text)))  
    print("  [*] fit transform success %s" %(int(time.time()-t_start)))
    text2digit_idx=0
    categoryDictIndex={} 
    for cat in category_dict:
        cnt=len(category_dict[cat])
        categoryDictIndex[cat]=text2digit[text2digit_idx:text2digit_idx+cnt]
        text2digit_idx+=cnt 

    vocabSize = len(text_vocab_processor.vocabulary_)
    if saveVocabTo!=None:
        text_vocab_processor.save(saveVocabTo)
    print("  [*] Time: %s" %(int(time.time()-t_start)))
    return categoryDictIndex,vocabSize,text_vocab_processor

if __name__=="__main__": 
    #list=GetDataList("Dataset/Data-Filtered_by_score_max_5")
    #print(list[4])
    print(clean_str("County Sheriff's Office and the"))