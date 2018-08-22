from Common import Utils,CategoryDataUtils
from   urllib.parse import urlsplit 
# Combine url/title/content as token

def regular(url,title,content):
    return title+" "+content

# Consider Host Name .host+title+content
def considerHost(url,title,content):
    x="%s %s %s" %(Utils.getHostFromUrl(url),title,content)
    return CategoryDataUtils.clean_str(x)

if __name__=="__main__":
    url="http://surveyequipment.com/terms-conditions/?SID=5qfgufld292o46ru39dhmeja62"
    title="Terms & Conditions"
    content="For's the purpose of this document \"Opti-cal Survey Equipment\" will be referred to by the abbreviation \"Opti-cal\". The information contained in this web site has been prepared solely "
    print(considerHost(url,title,content))