import re
def parseLine(line): 
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
    return category,url,title,content,subcategory

def run(infile,outfile):
    fin=open(infile,"rb")
    fout= open(outfile,"wb")
    while True:
        line=fin.readline().decode("utf-8")
        if line == "":
            break
        pos=[m.start() for m in re.finditer("\t",line)]
        fout.write((line[:pos[2]]+"\r\n").encode("utf-8"))
    return 

# create a file only contain url/category in order to  quick access by URLAnalyser
if __name__ == "__main__":
    infile="Dataset/Data_en-us_2017-05-30_2018-05-30_0_0.txt"
    #infile="Dataset/Data-9000"
    outfile=infile+"_only_url_catagory"
    run(infile,outfile)