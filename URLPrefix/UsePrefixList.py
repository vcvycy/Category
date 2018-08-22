from Trie import Trie
import utils
import sys
def getScore(msg,category):
    try:
        x=msg[1][category]
        return x*x/msg[0]
    except:
        return 0

def buildTrie(files):
    trie=Trie()
    for list in utils.filesLineIter(files): 
        if len(list)!=4:
            continue
        url=list[2]
        catNum={}
        sum=0 
        for item in list[3].split(" "):
            kv=item.split(":")
            kv[1]=int(kv[1])
            catNum[kv[0]]=kv[1]
            sum+=kv[1]
        trie.insert_merge(url,[sum,catNum]) 
    return trie 

def main(files):
    trie=buildTrie(files)
    url="https://www.ynetnews.com/articles/" 
    print("score: %s" %(trie.getScore(url,"rt_World")))

if __name__ == "__main__":
    prefix_files=["FinalData_2016-07-24_2017-07-23_12_12.txt_url_prefix_distribution_10_0.5_0_1000000",
                  "FinalData_2017-07-24_2018-07-24_12_12.txt_only_url_catagory_url_prefix_distribution_5_0.6_1000000_2000000",
                  "FinalData_2017-07-24_2018-07-24_12_12.txt_only_url_catagory_url_prefix_distribution_10_0.5_2000000_3000000",
                  "FinalData_2017-07-24_2018-07-24_12_12.txt_only_url_catagory_url_prefix_distribution_10_0.5_3000000_4000000"
                  ]
    main(prefix_files) 