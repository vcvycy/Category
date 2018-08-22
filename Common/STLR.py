######################################
## Slanted Triangular Learning Rate ## 
##            2018/08/09 by cjf@xmu ##
######################################
class STLR:
    def __init__(self, startLR=1e-3,maxLR=1e-2,maxLRAtStep=200,decayToStartLRAtStep=800,minLR=1e-5):
        self.startLR=startLR
        self.maxLR=maxLR
        self.maxLRAtStep=maxLRAtStep
        self.decayToStartLRAtStep=decayToStartLRAtStep
        self.minLR=minLR
        self.curStep=0
        return 
    def getLearningRate(self,step): 
        lr=0.0
        if step < self.maxLRAtStep:
            lr = step*(self.maxLR-self.startLR)/self.maxLRAtStep+self.startLR
        elif step < self.decayToStartLRAtStep:
            lr = (self.decayToStartLRAtStep-step)*(self.maxLR-self.startLR)/(self.decayToStartLRAtStep-self.maxLRAtStep)+self.startLR
        elif step < 4000:
            lr = 1e-3
        elif step <12000:
            lr = 1e-4
        elif step < 20000:
            lr=1e-5
        else:
            lr=1e-6
        return lr

if __name__=="__main__":
    stlr=STLR(1e-3,1e-2,20,140)
    for i in range (6001):
        print("Step:%d  lr=%s" %(i,stlr.getLearningRate(i)))