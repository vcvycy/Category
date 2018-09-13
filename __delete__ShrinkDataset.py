from Common import Utils
from Common import ArticleFilter
from Common import CategoryDataUtils

def getTruncatedContent(content,max_content_length):
    new_content="" 
    previous_char=" "  #forbit count continuous space 
    for ch in content:
        if ch==" " and previous_char!=" ":
            max_content_length-=1
        previous_char=ch
        new_content+=ch
        if max_content_length==0:
            break
    return new_content.strip()

# shrink data by limit sentence length
def process(in_file,out_file,max_content_length,max_size_per_category):
    print("[*]max size:%s" %(max_content_length))
    print("[*]%s -> %s" %(in_file,out_file))
    list=CategoryDataUtils.GetDataList(in_file)
    fout=open(out_file,"wb")
    category_cnt={}
    for category,url,title,content,subcategory in list:
        #
        if category not in category_cnt:
            category_cnt[category]=0 
        if category_cnt[category] >= max_size_per_category:
            continue
        category_cnt[category]+=1 
        #truncate content
        content=getTruncatedContent(content,max_content_length)
        line_out="%s\t%s\t%s\t%s\t%s\r\n" %(url,category,subcategory,title,content)
        line_out=line_out.encode("utf-8");  
        fout.write(line_out)
    fout.close()
    for cat in category_cnt:
        print("[*] %s :%d" %(cat,category_cnt[cat]))
    return 

if __name__=="__main__":
    max_content_length=500
    max_size_per_category=100000
    in_file="Dataset/FinalData_2016-07-24_2017-07-23_12_12.txt"
    #in_file="Dataset/tmp.txt"
    out_file="%s_maxlength_%s_max_per_category_%s" %(in_file,max_content_length,max_size_per_category)
    process(in_file,out_file,max_content_length,max_size_per_category)