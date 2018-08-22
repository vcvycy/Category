import sys
CHARACTER_SIZE=127
class Node:
    def __init__(self):
        self.next=[None for i in range(CHARACTER_SIZE)]
        self.msg=None 
        return

    def go(self,ch,createIfNotExist=False):
        if createIfNotExist and self.next[ord(ch)] == None:
            self.next[ord(ch)]=Node()
        return self.next[ord(ch)]
     
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
            return 0.5
        else:  
            x=msg[1][category]
            return x*x/msg[0] 