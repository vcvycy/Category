import re
entrylistPath=r"C:\Users\t-jianc\Documents\Visual Studio 2015\Projects\ScopeApplication2\ScopeApplication2\entry_list_60.txt"

def loadEntryList():
    f=open(entrylistPath,"rb")
    list=[]
    while True:
        line=f.readline().decode("utf-8");
        if line=="":
            break;
        pair=line.split("\t")
        list.append([pair[0].strip(),pair[1].strip()])
    return list

re_url_pattern=[
    #ping=60
    [r"thehill.com","rt_Politics"],
    [r"abcnews.go.com/Entertainment/","rt_Entertainment"]
    [r"nytimes.com/(\d\d\d\d)/(\d\d)/(\d\d)/sports/","rt_Sports"],
    [r"abcnews.go.com/Technology/","rt_ScienceAndTechnology"],
    [r"edition.cnn.com/(\d\d\d\d)/(\d\d)/(\d\d)/entertainment/","rt_Entertainment"],
    [r"edition.cnn.com/(\d\d\d\d)/(\d\d)/(\d\d)/sport","rt_Sports"],
    [r"money.cnn.com","rt_Business"],
    [r"www.foxsports","rt_Sports"],
    [r"marketwatch.com","rt_Business"],
    [r"msn.com/en-us/entertainment","rt_Entertainment"],
    [r"msn.com/en-us/news/technology","rt_ScienceAndTechnology"],
    [r"msn.com/en-us/sports/","rt_Sports"],
    [r"nasdaq.com","rt_Business"],
    [r"nbcnews.com/business/","rt_Business"],
    [r"politico.com","rt_Politics"],
    [r"",""],
    [r"",""],
    [r"",""],
    [r"",""],
    ]

def re_pattern_init():
    for i in range(len(re_url_pattern)):
        re_url_pattern[i][0]=re_url_pattern[i][0].replace(r"/",r"\/")
    # 
    urls=[
         r"https://www.nytimes.com/2018/08/12/sports/pga-championship-brooks-koepka-tiger-woods.html",
         r"https://edition.cnn.com/2018/08/10/entertainment/crazy-rich-asians-cast/index.html",
         r"https://abcnews.go.com/Entertainment/wireStory/foxs-ingraham-talking-race-57133508",
         r"http://thehill.com/policy/energy-environment/401355-zinke-takes-forest-fight-to-fire-ravaged-california",
         r"https://abcnews.go.com/Technology/wireStory/disney-results-fall-short-expectations-fox-bid-nears-57093297?cid=clicksource_79_2_hero_headlines_bsq_image",
         r"https://edition.cnn.com/2018/08/10/sport/winx-longines-rankings-no-1-spt-intl/index.html",
         r"https://money.cnn.com/2018/08/08/news/world/coffee-rust-honduras-colombia/index.html",
         r"https://www.foxsportsasia.com/football/asian-football/927116/asian-games-2018-lilipaly-double-gets-indonesia-up-and-running/",
         r"https://www.marketwatch.com/story/sp-500-is-stalling-but-these-3-sectors-are-scaling-fresh-highs-like-clockwork-2018-08-10",
         r"https://www.msn.com/en-us/tv/celebrity/2-days-before-his-death-bethenny-frankel-said-dennis-shields-wasnt-right-for-her/ar-BBLPLDn",
         r"https://www.msn.com/en-us/news/technology/vimeo-is-the-latest-platform-to-remove-content-from-infowars-conspiracy-theorist-alex-jones/ar-BBLQLVl",
         r"https://www.msn.com/en-us/sports/golf/pga-championship-2018-tiger-woods-didnt-win-the-pga-it-just-felt-like-he-did/ar-BBLQFh1",
         r"https://www.nasdaq.com/article/european-shares-set-to-follow-asian-peers-lower-20180813-00039",
         r"https://www.nbcnews.com/business/business-news/nyc-moves-rein-uber-cap-ride-hail-vehicles-n898976",
         r"https://www.politico.com/magazine/story/2018/08/12/charlottesville-anniversary-supremacists-protests-dc-virginia-219353",
         r"",
         r"",
         ]
    for item in re_url_pattern:
        pat=item[0]
        for url in urls: 
            if re.search(pat,url,re.IGNORECASE) != None:
                print("[*]MATCH %s %s" %(pat,url))
                 
# check if data is fit in list and regexp
def check(data,list): 
    # check by regexp
    for pattern,re_category in re_url_pattern:
        if re.match(pattern,url,re.IGNORECASE)!=None and re_category!=category:
            return False
    # pass check
    return True

def filter(infile,outfile):
    entrylist=loadEntryList()
    fin  = open(infile,"rb")
    fout = open(outfile,"wb")
    while True:
        line_in=fin.readline()
        print(line_in[:20])
        if line_in == b"":
            break; 
        if check(line_in.decode("utf-8"),entrylist): 
            fout.write(line_in) 
    fin.close()
    fout.close()

if __name__ == "__main__":
    re_pattern_init();
    #infile=r"C:\Users\t-jianc\Documents\Visual Studio 2015\Projects\ScopeApplication2\ScopeApplication2\NewsData.txt"
    #outfile=r"C:\Users\t-jianc\Documents\Visual Studio 2015\Projects\ScopeApplication2\ScopeApplication2\tmp.txt"
    #filter(infile,outfile)