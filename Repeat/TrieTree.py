import sys
CHARACTER_SIZE=27
def index(ch): 
      asc=ord(ch)
      if asc<=122 and asc>=97:  # a~z
        return asc-97 
      if asc<=90 and asc>=65:   # A~Z
          return asc-65
      return 26

class Node:
    def __init__(self):
        self.next=[None for i in range(CHARACTER_SIZE)]
        self.msg=None 
        return

    def go(self,idx,createIfNotExist=False):
        if createIfNotExist and self.next[idx] == None:
            self.next[idx]=Node()
        return self.next[idx]

class Trie: 
    def __init__(self):
        self.root=Node()
        return

    def insert(self,str,msg):
        str=str.strip();
        cur_node=self.root;
        for ch in str:
            idx=index(ch)
            cur_node = cur_node.go(idx,True)
        cur_node.msg = msg
        return

    # Find first string in trie ,then return msg. else return None
    def find(self,str):
        str=str.strip();
        cur_node=self.root
        for ch in str:
            idx=index(ch)
            cur_node = cur_node.go(idx)
            if cur_node == None:
                return None
        return cur_node.msg
