import  pandas as pd
import  numpy as np

rootPath = '../../../'

class ProjDataDump():
    def __init__(self):
        self.inputDataPath = rootPath + 'Data/Variables/Whole/ProjAnalysis/Proj_Importance.csv'
        self.outputDataPath = rootPath + 'Data/Variables/Whole/ProjAnalysis/Proj_NumID.csv'
        self.mainDataList = self.loadData()
        self.mainDataListSorted = self.sortData()
        self.fileDump()

    def loadData(self):
        retList = []
        f = open(self.inputDataPath,'r')
        while True:
            line = f.readline()
            if not line: break
            data = line.rstrip('\n').split('|')
            data = data[0].split(',')
            retList.append([data[0],data[1],data[3]])
        f.close()
        return retList

    def sortData(self):
        retList = []
        numID = []
        for lst in self.mainDataList:
            numID.append(int(lst[2]))
        sortedIndex = np.argsort(numID)[::-1]
        for idx in sortedIndex:
           retList.append(self.mainDataList[idx])
        return retList

    def fileDump(self):
        f = open(self.outputDataPath,'w')
        for data in self.mainDataListSorted:
            f.write('%s,%s,%s\n'%(data[0],data[1],data[2]))
        f.close()

def Main():
    instance = ProjDataDump()


if __name__ == '__main__':
    Main()