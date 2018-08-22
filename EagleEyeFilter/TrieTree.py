CHARACTER_SIZE=127
class Node:
    def __init__(self):
        self.next=[None for i in range(CHARACTER_SIZE)]
        self.msg=None
        self.failed=None
        return

    def go(self,ch,createIfNotExist=False):
        if createIfNotExist and self.next[ord(ch)] == None:
            self.next[ord(ch)]=Node()
        return self.next[ord(ch)]

class Trie: 
    def __init__(self):
        self.root=Node()
        return

    def insert(self,str,msg):
        cur_node=self.root;
        for ch in str:
            cur_node = cur_node.go(ch,True)
        cur_node.msg = msg
     
    # Find first string in trie ,then return msg. else return None
    def findUntilEndpoint(self,str):
        cur_node=self.root
        for ch in str:
            cur_node = cur_node.go(ch)
            if cur_node == None:
                return None 
            if cur_node.msg != None:
                return cur_node.msg
        return None

    def getPrefixCategory(self,str):
        cur_node=self.root
        for ch in str:
            cur_node=cur_node.go(ch)
            if cur_node==None:
                return None
            if cur_node.msg!=None:
                return cur_node.msg
        print("[*]unkown reason:%s " %(str))   # url is prefix of some entrylist
        return None
             
