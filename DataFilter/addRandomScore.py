# used to randomly select some news
import utils
import random
def main(infile,outfile):
    fout=open(outfile,"wb")
    for item in utils.fileLineIter(infile):
        score=random.randint(0,1000000)
        item.append(score)
        fout.write(utils.mergeToLine(item).encode("utf-8"))
    return

if __name__=="__main__":
    infile="Dataset/NewsFeatures_2018_08_27_17.txt"
    outfile=infile+"_RandomScore"
    main(infile,outfile)