import utils 
def showCategoryDistribution(infile):
    cnt={}
    total=0
    for list in utils.filesLineIter(infile):
        if len(list)<3:
            print("[*]break")
            break
        url=list[0]
        category=list[1]
        subcat=list[2] 
        if category not in cnt:
            cnt[category]=[0,{}] 
        #category
        total+=1
        cnt[category][0]+=1
        if subcat!="":
            if subcat not in cnt[category][1]:
                cnt[category][1][subcat]=0
            cnt[category][1][subcat]+=1 
            if category=="rt_Business":
                print(list)
                input("")
    print("\n[*]files:%s" %(infile))
    #show
    for cat in cnt:
        print("[*] %s :%s %.2f%%" %(cat,cnt[cat][0],cnt[cat][0]/total*100))
        cnt_sub=cnt[cat][1]
        unclassified=cnt[cat][0]
        for subcat in cnt_sub:
            share=cnt_sub[subcat]/cnt[cat][0]
            print("  [*]%s :%s  [share:%s]" %(subcat,cnt_sub[subcat],share))
            unclassified-=cnt_sub[subcat]
        if len(cnt_sub)>0:
            print("  [*]----Left:%s %s----" %(unclassified,unclassified/cnt[cat][0]))

    return
if __name__ == "__main__":
    #file="news_del_Data-Filtered_files_3_desc_by_length"
    #file="NewsFeatures_2018_08_27_17_Random30_Origin"
    #file ="NewsFeatures_2018_08_27_17.txt"
    file="raw/AllDataRaw_TitleRepeat"
    showCategoryDistribution(file)
