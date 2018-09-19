from DataFilter import utils
from Common import ArticleFilter
from Common import CategoryDataUtils
import random 
import time 
import tensorflow as tf
import numpy as np 
fout=None
def myprint(str):
    global fout
    str+='\n'
    fout.write(str.encode("utf-8"))
def main(infile,ignore_case):
    # text
    text=[]
    for item in utils.fileLineIter(infile):
        url=item[0]
        category=item[1]
        subcat=item[2]
        title=item[3]
        content=item[4]
        #text.append(title+" "+content)
        cleaned_text=CategoryDataUtils.clean_str(title+" "+content)
        text.append(cleaned_text)
    
    vocabproc = tf.contrib.learn.preprocessing.VocabularyProcessor(400,min_frequency=20)  
    vocabproc.fit_transform(text) 
    vp_size=len(vocabproc.vocabulary_)  
    inner={}
    # google model
    with open("Dataset/GoogleNews-vectors-negative300.bin", "rb") as f:
        header = f.readline()
        vocab_size, layer1_size = map(int, header.split())
        print("  [*]Google:vocab_size:%s" %(vocab_size)) 
        binary_len = np.dtype('float32').itemsize * layer1_size
        for line in range(vocab_size):
            word = []
            while True:
                ch = f.read(1).decode('latin-1')
                if ch == ' ':
                    word = ''.join(word)
                    break
                if ch != '\n':
                    word.append(ch)
            if ignore_case:
               word=word.lower()
            idx = vocabproc.vocabulary_.get(word) 
            f.read(binary_len)
            if idx != 0: 
                inner[word]=True 
            #myprint("%s " %(word))

    myprint("Inner join/Total Vocabulary : %s/%s\n" %(len(inner),len(vocabproc.vocabulary_))) 
    myprint("Word Not In Google Word2Vec:")
    for word in vocabproc.vocabulary_._mapping:
        if word not in inner:
            myprint(word) 
    
    myprint("Word In Google Word2Vec:")
    for word in vocabproc.vocabulary_._mapping:
        if word in inner:
            myprint(word) 
    return 

if __name__ == "__main__":
    #infile="Dataset/AllData_TitleRepeat_add_score_getTop_200000_CleanText"
    infile="Dataset/Data-9000"
    fout=open(infile+"_wordvec_join.txt","wb")
    ignore_case=True
    main(infile,ignore_case)