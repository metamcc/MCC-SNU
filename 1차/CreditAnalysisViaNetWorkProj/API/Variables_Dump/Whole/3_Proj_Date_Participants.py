import  pandas as pd
import  numpy as np

rootPath = '../../../'

class Proj_Date_Participants():
    def __init__(self):
        self.inputDataPath = rootPath + 'Data/RawData'
        self.inputDataPath1 = rootPath + 'Data/Prj_List.csv'
        self.outputDataPath = rootPath + 'Data/Variables/Whole/ProjAnalysis/Proj_Date_Participants.csv'
        self.projList = self.loadProjList()
        self.mainDatadf = self.loadData()
        self.proj_Date_Dict = self.make_Proj_Date_Dict()
        self.fileDump()

    def loadData(self):
        period = [2015,2016,2017]
        df_main = pd.DataFrame([],columns=['emp_id', 'emp_name', 'dact_date', 'prj_id', 'prj_name', 'pact_rate',
       'pact_desc', 'pact_rstar'])
        for year in period:
            filename = self.inputDataPath + '/HR_pace 프로젝트 참여도_' + str(year) + '.csv'
            df = pd.read_csv(filename)
            df_main = pd.concat([df_main,df])
        return df_main

    def loadProjList(self):
        retList = []
        f = open(self.inputDataPath1,'r')
        while True:
            line = f.readline()
            if not line: break
            data = line.rstrip('\n').split(',')
            retList.append(data[0])
        f.close()
        return retList

    def make_Proj_Date_Dict(self):
        retDict = {}
        for index,row in self.mainDatadf.iterrows():
            if not row.prj_id in retDict.keys():
                retDict[row.prj_id] = {}
            if not row.dact_date in retDict[row.prj_id].keys():
                retDict[row.prj_id][row.dact_date] = []
            retDict[row.prj_id][row.dact_date].append(row.emp_id)
        # for key, value in retDict.items():
        #     retDict[key] = sorted(set(value))
        return retDict

    def fileDump(self):
        f = open(self.outputDataPath,'w')
        for key in sorted(self.proj_Date_Dict.keys()):
            f.write('%s:'% key)
            lenData = len(self.proj_Date_Dict[key].keys())
            for idx,key1 in enumerate(sorted(self.proj_Date_Dict[key].keys())):
                f.write('%s|'% key1)
                i = 0
                while i < (len(self.proj_Date_Dict[key][key1])-1):
                    f.write('%s,'% self.proj_Date_Dict[key][key1][i])
                    i += 1
                if idx != (lenData-1):
                    f.write('%s&'% self.proj_Date_Dict[key][key1][i])
                else:
                    f.write('%s'% self.proj_Date_Dict[key][key1][i])
            f.write('\n')
        f.close()




def Main():
    Proj_Date_Participants()


if __name__ == '__main__':
    Main()