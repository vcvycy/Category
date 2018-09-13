class Heap:
    def __init__(self,max_size,cmp):
        self.max_size=max_size
        self.size=0
        #self.data start from 1 (1->max_size)
        self.data=[None for _ in range(max_size+1)]
        self.cmp=cmp
        return
    # insert min-heap
    def insert(self,item): 
        #print("[*] insert %s" %(item))
        if self.size == self.max_size:
            if self.cmp(item,self.data[1]):
                return
            self.pop()
        self.size+=1
        self.data[self.size]=item
        idx=self.size
        while idx>0:
            self.maintain(idx)
            idx=idx>>1
        return
    
    def pop(self): 
        #print("[*] pop %s" %(self.data[1]))
        self.data[1]=self.data[self.size]
        self.data[self.size]=None
        self.size-=1
        self.maintain(1)
        return 

    def maintain(self,i):
        if i*2 > self.size:
            return
        min_idx=i*2
        if i*2+1 <= self.size and self.cmp(self.data[i*2+1],self.data[i*2]):
            min_idx=i*2+1
        if self.cmp(self.data[min_idx],self.data[i]):
            self.data[min_idx],self.data[i]=self.data[i],self.data[min_idx]
            self.maintain(min_idx)
        return 

    def enum(self):
        while self.size>0:
            yield self.data[1]
            self.pop()
        return

    def enum_all(self):
        for i in range(1,self.size+1):
            yield self.data[i]
        
        return

# Test
def cmp(x,y): 
    return x<=y
if __name__== "__main__":
    heap=Heap(5,cmp)
    l=[1 for i in range(10)]
    for i in l:
        heap.insert(i)
    for item in heap.enum():
        print(item)