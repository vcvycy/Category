import tensorflow as tf
import numpy as np
import os
import datetime
import time
from TextRCNN import TextRCNN 
from Common.STLR import STLR
from Common import Utils
from MyData import MYData
import sys 

def getParameterNumbers():
    total_parameters = 0
    for variable in tf.trainable_variables():
        # shape is an array of tf.Dimension
        shape = variable.get_shape() 
        variable_parameters = 1
        for dim in shape:
            variable_parameters *= dim.value 
        total_parameters += variable_parameters
    return total_parameters

def solver(mydata,config):
    #output dir
    timestamp =  time.strftime('%Y-%m-%d-%Hh-%Mm-%Ss')
    out_dir = os.path.abspath(os.path.join(os.path.curdir, "runs", timestamp))
    print("Writing to {}\n".format(out_dir))
    #get RCNN 
    rcnn=TextRCNN(
        sequence_length=config["sequence_length"],
        num_classes=mydata.getClasses(),
        vocab_size=mydata.vocabSize,
        word_embedding_size=config["word_embedding_size"],
        context_embedding_size=config["context_embedding_size"],
        cell_type=config["cell_type"],
        hidden_size=config["hidden_size"],
        l2_reg_lambda=config["l2_reg_lambda"],
        W_text_trainable=config["W_text_trainable"],
        out_dir=out_dir
        ) 
    ## summary
    sess=rcnn.sess

    # Checkpoint directory. Tensorflow assumes this directory already exists so we need to create it
    checkpoint_dir = os.path.abspath(os.path.join(out_dir, "checkpoints"))
    checkpoint_prefix = os.path.join(checkpoint_dir, "model")
    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)
        
    #save vocab/config/category
    mydata.saveCategory2Index(os.path.join(out_dir,"category_index"))
    mydata.vocabproc.save(os.path.join(out_dir, "text.vocab"))
    Utils.showAndSaveConfig(config,os.path.join(out_dir, "config.txt"))

    print("[*]parameter number: %s" %(getParameterNumbers()))

    saver = tf.train.Saver(tf.global_variables(), max_to_keep=10) 

    # Initialize all variables
    sess.run(tf.global_variables_initializer())

    restore_from=config["restore_from"]
    if restore_from!=None:
        saver.restore(sess,restore_from)
        print("[*]restore success")
    # Pre-trained word2vec
    if config["LoadGoogleModel"] and restore_from==None: 
        print("[*]Loading Google Pre-trained Model")
        # initial matrix with random uniform
        initW = np.random.uniform(-0.25, 0.25, (mydata.vocabSize, config["word_embedding_size"]))
        # load any vectors from the word2vec
        word2vec=config["Word2Vec"]
        print("  [*]Load word2vec file {0}".format(word2vec))
        cnt_word_in_word2vec=0   
        with open(word2vec, "rb") as f:
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
                idx = mydata.vocabproc.vocabulary_.get(word)
                if idx != 0:
                    initW[idx] = np.fromstring(f.read(binary_len), dtype='float32')
                    cnt_word_in_word2vec+=1
                else:
                    f.read(binary_len) 
            print("  [*]Load Google Model success: word in Word2Vec :%s total word:%s" 
                  %(cnt_word_in_word2vec,mydata.vocabSize))

        sess.run(rcnn.W_text.assign(initW))
        print("[*]Success to load pre-trained word2vec model!\n")
         
    # start traning 
    # step && learning rate
    stlr=STLR(1e-3,1e-2,200,600)
    step=0
    while True:
        batch=mydata.nextBatch(config["BatchSize"])
        learning_r=stlr.getLearningRate(step)
        feed_dict = {
            rcnn.input_text: batch[0],
            rcnn.input_y: batch[1],
            rcnn.dropout_keep_prob: config["droupout"],
            rcnn.learning_rate:learning_r
        }
        _, step, summaries, loss, accuracy = sess.run(
            [rcnn.train_op, rcnn.global_step, rcnn.train_summary_op, rcnn.loss, rcnn.accuracy], feed_dict)
        rcnn.summary_writer.add_summary(summaries, step)
        # Training log display
        if step % config["TraingLogEverySteps"] == 0:
            time_str = datetime.datetime.now().isoformat() 
            print("  [*] step %s;  loss %s;  acc %s; lr %.6f " %(step,loss,accuracy,learning_r))

        # Evaluation
        if  step % config["TestEverySteps"] == 0:
            test_data=mydata.getTestData()
            test_size=len(test_data[0])  
            correct_predict_count=0
            dev_loss=0
            for i in range(0,test_size,500):
                x_test=test_data[0][i:i+500] 
                y_test=test_data[1][i:i+500] 
                feed_dict_dev = {
                    rcnn.input_text: x_test,
                    rcnn.input_y: y_test,
                    rcnn.dropout_keep_prob: 1.0
                }
                summaries_dev, loss, accuracy = sess.run([rcnn.dev_summary_op, rcnn.loss, rcnn.accuracy], feed_dict_dev)
                #rcnn.summary_writer.add_summary(summaries_dev, step)
                #
                correct_predict_count+=int(0.5 + accuracy*len(x_test))
                dev_loss+=loss*len(x_test)/test_size
            #dev summary
            dev_accuracy=correct_predict_count/test_size 

            rcnn.summary_writer.add_summary(tf.Summary(value=[tf.Summary.Value(tag="dev_loss",simple_value= dev_loss)]),step)
            rcnn.summary_writer.add_summary(tf.Summary(value=[tf.Summary.Value(tag="dev_accu",simple_value= dev_accuracy)]),step)
            time_str = datetime.datetime.now().isoformat()
            print("\n[*]Test:%s step %s, loss %.6f, acc %.6f " %(time_str, step, dev_loss, dev_accuracy))

        # Model checkpoint
        if step % 1000 == 0:
            path = saver.save(sess, checkpoint_prefix, global_step=step)
            print("Saved model checkpoint to {}\n".format(path))

if __name__ == "__main__": 
    config={
        "cell_type":"gru",  # vanilla/lstm/gru
        "sequence_length":400, 
        "word_embedding_size":300,
        "context_embedding_size":300,
        "hidden_size":512,
        "droupout":0.7,    # used in tensorflow
        "l2_reg_lambda":1e-4,
        #google model
        "LoadGoogleModel":True,
        "Word2Vec":"Dataset/GoogleNews-vectors-negative300.bin", 
        "W_text_trainable":True,
        # word min frequence
        "min_frequence":10,
        "article_droup_out":1.0,  # used to 
        "TraingLogEverySteps":10,
        "TestEverySteps":100, 
        "restore_from":None,
        #"restore_from":r"runs\2018-08-15-14h-22m-44s\checkpoints\model-100",
        #dataset
        "trainning_data":["Dataset/Data-9000","Dataset/Data-9000"]
        #"trainning_data":"Dataset/FinalData_2017-07-24_2018-07-24_12_12.txt_maxlength_500_max_per_category_100000_EagleEye-1" 
        }
     
    mydata=MYData(config["trainning_data"],
                  minSizePerCategory=10,
                  max_article_length=config["sequence_length"],
                  min_frequence=config["min_frequence"],
                  training_share= 0.9,
                  droup_out=config["article_droup_out"]           # will random remove word from article
                  ) 
    config["BatchSize"]=mydata.getClasses()*4;
    config["vocabSize"]=mydata.vocabSize;
    config["classes"]=mydata.getClasses()
    solver(mydata,config)
