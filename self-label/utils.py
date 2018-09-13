import re
import time
def parseLineAllItems(line): 
    pos=[m.start() for m in re.finditer("\t",line)]
    if len(pos)<4:
        Utils.error("len(pos)<4")
    url=line[0:pos[0]]
    category=line[pos[0]+1:pos[1]]
    subcategory=line[pos[1]+1:pos[2]]
    title=line[pos[2]+1:pos[3]]
    content=line[pos[3]+1:]
    #
    url=url.strip()
    category=category.strip()
    title=title.strip()
    content=content.strip()
    subcategory=subcategory.strip()
    return url,category,subcategory,title,content

def getListSplitByTab(line):
    pos=[m.start() for m in re.finditer("\t",line)]
    list=[]
    list.append(line[0:pos[0]])
    for idx in range(0,len(pos)-1):
        list.append(line[pos[idx]+1:pos[idx+1]])
    list.append(line[pos[len(pos)-1]+1:])

    for i in range(len(list)):
        list[i]=list[i].strip() 
    return list

def mergeToLine(items):
    line=""
    for idx in range(len(items)):
        line+=items[idx]
        if idx!=len(items)-1:
            line+="\t"
        else:
            line+="\r\n"
    return line

# iteration of by f.readline
def fileLineIter(f):
    if type(f)==type(""):
        f=open(f,"rb")
    while True:
        line=f.readline().decode("utf-8")
        if line=="":
            break 
        yield getListSplitByTab(line)
    return

def filesLineIter(files):
    for file in files:
        try:
            f=open(file,"rb")
        except:
            f=open("Dataset/"+file,"rb")
        while True:
            line=f.readline().decode("utf-8")
            if line=="":
                break
            yield getListSplitByTab(line)
    return

#read data from filename
def GetDataList(filename): 
    t_start=time.time()
    list=[]
    try:
        f=open(filename,"rb")
    except: 
        f=open("Dataset/"+filename,"rb")
    while True:
        line=f.readline().decode("utf-8")
        if line!="":
            list.append(parseLineAllItems(line))
        else:
            break
    print("  [*]Get Data List %s Time: %s" %(filename,int(time.time()-t_start)))
    return list
 

def parseLine(line): 
    pos=[m.start() for m in re.finditer("\t",line)]
    if len(pos)<2:
        Utils.error("len(pos)<2")
    url=line[0:pos[0]]
    category=line[pos[0]+1:pos[1]]
    if len(pos)==2:
        pos.append(len(line))
    subcategory=line[pos[1]+1:pos[2]] 
    #
    url=url.strip()
    category=category.strip() 
    subcategory=subcategory.strip()
    return url,category,subcategory

def showCategoryDistribution(infile):
    cnt={}
    fin=open(infile,"rb")
    while True: 
        line=fin.readline().decode("utf-8")
        if line=="":
            break
        url,category,subcat=parseLine(line)
        if category not in cnt:
            cnt[category]=[0,{}] 
        #category
        cnt[category][0]+=1
        if subcat!="":
            if subcat not in cnt[category][1]:
                cnt[category][1][subcat]=0
            cnt[category][1][subcat]+=1 
    #show
    for cat in cnt:
        print("[*] %s :%s" %(cat,cnt[cat][0]))
        cnt_sub=cnt[cat][1]
        for subcat in cnt_sub:
            print("  [*]%s :%s" %(subcat,cnt_sub[subcat]))
    return


if __name__ == "__main__":
    for list in fileLineIter("Dataset/Data-9000"):
        print(list)