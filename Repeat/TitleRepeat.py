from  TrieTree import Trie
import utils
"""
# TOO SLOW
def main(infile,outfile,title_idx): 
    trie=Trie()
    repeat_count=0
    total=0
    f_out=open(outfile,"wb")

    for item in utils.fileLineIter(file):
        total+=1
        title=item[title_idx]
        if len(title)>70:
          title=title[:70]
        if trie.find(title)==None:  
            trie.insert(title,True)
            f_out.write(utils.mergeToLine(item).encode("utf-8"))
        else:
            repeat_count+=1
    print("[*]repeat_count:%s/%s" %(repeat_count,total))
    return
"""
def main(infile,outfile,title_idx=3): 
    trie=Trie()
    repeat_count=0
    total=0
    f_out=open(outfile,"wb")
    s=set()
    for item in utils.filesLineIter(infile):
        total+=1
        title=item[title_idx].strip().lower() 
        if title not in s: 
            s.add(title)
            f_out.write(utils.mergeToLine(item).encode("utf-8"))
        else:   
            repeat_count+=1
    print("[*]repeat News :%s total:%s" %(repeat_count,total))
    return
if __name__== "__main__":
    # read news from file. remove news that has same title
    files=["AllDataPlus_TitleRepeat_add_score_getTop_250000",
           "raw/AllDataRaw_TitleRepeat_add_score_getTop_80000"
           ]
    out_file="Dataset/AllDataPlus_merge_raw80000"
    main(files,out_file)