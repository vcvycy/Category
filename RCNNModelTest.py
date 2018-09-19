import tensorflow as tf
import numpy as np
import os
import datetime
import time
from TextRCNN import TextRCNN 
import sys
import io
#import DataLoader
import os
from Common import CategoryDataUtils,Utils    
def restore_from_lastest(sess,saver,root):
    path=os.path.join(root,"checkpoints")
    for i in range(60,1,-1):
        p=os.path.join(path,"model-%d" %(i*1000)) 
        try:
            saver.restore(sess,p)
            print("[*]restore from %s" %(p))
            return
        except:
            continue
    print("[!]can't restore")
    sys.exit(-1)
    return

class ModelTest():
    def __init__(self,root):
        self.root=root   # model directory
        self.sess=tf.Session()
        idx2cat=self.load_idx2cat() 
        self.rcnn,self.vocabproc=self.load_model()   
        return

    def getParameterNumbers(self):
        total_parameters = 0
        for variable in tf.trainable_variables():
            # shape is an array of tf.Dimension
            shape = variable.get_shape() 
            variable_parameters = 1
            for dim in shape:
                variable_parameters *= dim.value 
            total_parameters += variable_parameters
        return total_parameters
 
    def softmax(self,a):
        return np.exp(a)/np.sum(np.exp(a))

    def load_idx2cat(self):
        filename=os.path.join(self.root,"category_index")
        f=open(filename)
        idx2cat={}
        while True:
            line=f.readline()
            if line=="":
                break
            kv=line.strip().split(":")
            idx2cat[int(kv[0])]=kv[1]
            print("[*] %s -> %s" %(kv[0],kv[1]))
        self.idx2cat=idx2cat
        return idx2cat

    def load_config(self):
        filename=os.path.join(self.root,"config.txt")
        f=open(filename)
        config={}
        while True:
            line=f.readline().strip()
            if line=="":
                break
            if line[0]=="=":
                continue
            kv=line.split(" ")[-1].split(":")
            key=kv[0].strip()
            try:
                value=int(kv[1])
            except:
                try:
                    value=float(kv[1])
                except:
                    if kv[1]=="True":
                        value=True
                    if kv[1]=="False":
                        value=False 
                    value=kv[1]
            config[key]=value
            print("%s = %s" %(key,value))
        return config 
     
    def load_model(self):   
        config=self.load_config()
        vocabproc = tf.contrib.learn.preprocessing.VocabularyProcessor.restore(os.path.join(self.root,"text.vocab"))
        print("Text Vocabulary Size: {:d}".format(len(vocabproc.vocabulary_)))   

        rcnn=TextRCNN(
            sequence_length=config["sequence_length"],
            num_classes=config["classes"],
            vocab_size=len(vocabproc.vocabulary_),
            word_embedding_size=config["word_embedding_size"],
            context_embedding_size=config["context_embedding_size"],
            cell_type=config["cell_type"],
            hidden_size=config["hidden_size"],
            l2_reg_lambda=config["l2_reg_lambda"],
            W_text_trainable=config["W_text_trainable"]
            ) 
        self.sess.run(tf.global_variables_initializer())  
        saver = tf.train.Saver() 
        restore_from_lastest(self.sess,saver,self.root) 
        return rcnn,vocabproc

    def _predict(self,text_list):
        if type(text_list)==type(""):
            text_list=[text_list]
        text_list = CategoryDataUtils.textListPreprocess(text_list) #clean str 
        vec=np.array(list(self.vocabproc.transform(text_list))) 
        feed_dict={
            self.rcnn.input_text: vec,
            self.rcnn.dropout_keep_prob:1.0 
            }
        predictions,prob = self.sess.run([self.rcnn.predictions,self.rcnn.prob], feed_dict)
        result=[]
        for item in prob:
            cur_article={}
            for i in range(len(item)):
                cur_article[self.idx2cat[i]]=item[i]
            result.append(cur_article)
        return result 

    def predict(self,text_list,preserve_words=400):
        if type(text_list)==type(""):
            text_list=[text_list] 
        text_list = [CategoryDataUtils.clean_str(sent) for sent in text_list]
        vec=np.array(list(self.vocabproc.transform(text_list))) 
         
        for i in range(len(vec)):
            for j in range(preserve_words,400):
                vec[i][j]=0 
        result=[]
        print("[*]transform success");
        for i in range(0,len(vec),500):
            feed_dict={
                self.rcnn.input_text: vec[i:i+500],
                self.rcnn.dropout_keep_prob:1.0 
                }
            predictions,prob = self.sess.run([self.rcnn.predictions,self.rcnn.prob], feed_dict) 
            for item in prob:
                cur_article={}
                for j in range(len(item)):
                    cur_article[self.idx2cat[j]]=item[j]
                result.append(cur_article)
            print("[*]progress:%d/%d" %(i,len(vec)))
        return result 

    def predict_split(self,text_list):
        if type(text_list)==type(""):
            text_list=[text_list]
        text_list = CategoryDataUtils.textListPreprocess(text_list) #clean str 
        _vec=list(self.vocabproc.transform(text_list))
        partNum=1
        partSize=int(400/partNum)
        vec=[]
        for item in _vec: 
            for i in range(partNum):
                tmp=item.copy()
                for j in range(400):
                    if j>partSize*i and j< partSize*(i+1):
                        tmp[j]=0 
                vec.append(tmp)
        vec=np.array(vec)
        print(len(vec))
        result=[]
        print("[*]transform success");
        for i in range(0,len(vec),500):
            feed_dict={
                self.rcnn.input_text: vec[i:i+500],
                self.rcnn.dropout_keep_prob:1.0 
                }
            predictions,prob = self.sess.run([self.rcnn.predictions,self.rcnn.prob], feed_dict) 
            for item in prob:
                cur_article={}
                for j in range(len(item)):
                    cur_article[self.idx2cat[j]]=item[j]
                result.append(cur_article)
            print("[*]progress:%d/%d" %(i,len(vec)))
        #merge
        _result=[]
        for i in range(0,len(result),partNum):
            _result.append(merge_result_mean(result[i:i+partNum]))
            
        return _result 

def merge_result_mean(r):
    # 取平均
    rst={}
    cats={}
    for cat in r[0]:
        rst[cat]=r[0][cat]
        for i in range(1,len(r)):
            rst[cat]+=r[i][cat]
        rst[cat]/=len(r)
    return rst


category_set={
        "rt_Entertainment",
        "rt_Politics",
        "rt_Sports",
        "rt_US",
        "rt_Business",
        "rt_ScienceAndTechnology",
        "rt_World", 
        "rt_Health"
        }
if __name__ == "__main__":
    #main(r"runs\83_step_25000")
    #dir="runs/83_step_25000"
    dir="runs/TitleRepeat_92+"
    #dir="runs/88.5_prefix_filter"
    model=ModelTest(dir) 
    while True:
        text1=input("\n[*]Input Article")
        result=model.predict([text1])
        print(result) 
        getFourth(result[0])