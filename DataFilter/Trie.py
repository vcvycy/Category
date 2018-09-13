import sys
CHARACTER_SIZE=127 
def char2idx(ch): 
    asc=ord(ch)
    if asc>=48 and asc<=57:
        return 48 
    return ord(ch)

def idx2char(idx): 
    return chr(idx)

class Node:
    def __init__(self):
        self.next=[None for i in range(CHARACTER_SIZE)]
        self.msg=None 
        return
    
    def go(self,ch,createIfNotExist=False): 
        idx=char2idx(ch)
        if createIfNotExist and self.next[idx] == None:
            self.next[idx]=Node() 
        if idx>CHARACTER_SIZE:
            return None
        else:
            return self.next[idx] 
     
class Trie: 
    def __init__(self):
        self.root=Node()
        return

    def insert_merge(self,str,msg):
        cur_node=self.root;
        for ch in str:
            cur_node = cur_node.go(ch,True)
        if cur_node.msg==None:
            cur_node.msg = msg
        else: 
            cur_node.msg[0]+=msg[0]
            for cat in msg[1]:
                if cat not in cur_node.msg[1]:
                    cur_node.msg[1][cat]=0
                cur_node.msg[1][cat]+=msg[1][cat] 
    # Find first string in trie ,then return msg. else return None
    def find(self,str):
        cur_node=self.root
        for ch in str:
            cur_node = cur_node.go(ch)
            if cur_node == None:
                return None 
            if cur_node.msg != None:
                return cur_node.msg
        return None 
             
    def getScore(self,str,category):  
        msg=self.find(str)
        if msg==None or category not in msg[1]:
            return 0.4
        else:  
            unclassified_cnt=0
            if "rt_Unclassified" in msg[1]:
                unclassified_cnt=msg[1]["rt_Unclassified"]
            if (msg[0]-unclassified_cnt<10):
                return 0.4
            x=msg[1][category]
            return x/(msg[0]-unclassified_cnt) 