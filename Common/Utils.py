import sys
from urllib.parse import urlsplit

def showAndSaveConfig(config,filename=None):
    text= "===CONGIGURATION===\n" 
    for key in config:
        text+="  [*] %s:%s\n" %(key,config[key]) 
    text+="=========END=======\n"
    print(text)
    if filename!=None: 
        f=open(filename,"w")
        f.write(text)
        f.close()

def error(msg):
    print("[*]Error:%s" %(msg))
    sys.exit(0)

def getHostFromUrl(url):
    return "{0.netloc}".format(urlsplit(url))

if __name__=="__main__":
    url="http://surveyequipment.com/terms-conditions/?SID=5qfgufld292o46ru39dhmeja62"
    print(getHostFromUrl(url))