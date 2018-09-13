import utils
import json


def change(dict,cat,subcat):
    if subcat!=None:
        name="%s/%s" %(cat,subcat)
    else:
        name="%s" %(cat)
    if name in dict:
    else:
        return cat,subcat 

def main(file_in,file_out,jsonfile):
    try:
      jf=open("DataFilter/"+jsonfile,"r")
    except:
      jf=open(jsonfile,"r")
    dict_cat=json.loads(jf.read())
    print(dict_cat)
#    f_out=open(file_out,"wb")
    #for list in utils.fileLineIter(file_in):
    #    list

if __name__ == "__main__":
    jsonfile="change_category.json"
    file_in="Data-9000"
    file_out=file_in+"_%s" %(jsonfile)
    main(file_in,file_out,jsonfile)
