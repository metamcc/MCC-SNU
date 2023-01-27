import  pandas as pd
import  numpy as np

rootPath = '../../../'

class EmpDataDump():
    def __init__(self):
        self.yearList = yearList = [2015,2016,2017]
        self.inputDataPath = rootPath + 'Data/RawData'
        self.inputDataPath2 = rootPath + 'Data'
        self.outputDataPath = rootPath + 'Data/Variables/Yearly/EmpAnalysis'
        self.main_df = self.loadData()
        self.fileDump()
    #
    # def make_prj_id_name_dict(self):
    #     retDict = {}
    #     filename = self.inputDataPath2 + '/Prj_List.csv'
    #     f = open(filename,'r')
    #     while True:
    #         line = f.readline()
    #         if not line: break
    #         data = line.rstrip('\n').split(',')
    #         retDict[data[0]] = data[1]
    #     return retDict

    def loadData(self):
        retList = []
        tpRetListContainer = []
        proj_pact_rate_List = []

        filename = self.inputDataPath + '/직원테이블.csv'
        df = pd.read_csv(filename)
        for i in range(len(df.leave_date)):
            try:
                df.leave_date[i] = int(df.leave_date[i])
            except:
                df.leave_date[i] = 99999999
        for i in range(len(df.wedding_day)):
            try:
                df.wedding_day[i] = int(df.wedding_day[i])
            except:
                df.wedding_day[i] = 99999999
        return df

    def fileDump(self):
        for year in self.yearList:
            yearData = self.main_df[((self.main_df.entry_date < (year+1)*10000) & (self.main_df.leave_date > year*10000))]
            filename = self.outputDataPath + '/EmpProfile_' + str(year) + '.csv'
            f = open(filename,'w')
            for index,row in yearData.iterrows():
                for i in range(9):
                    f.write('%s'%(row[i]))
                    if not (i == 8):
                        f.write(',')
                    else:
                        f.write('\n')
            f.close()
def Main():
    instance = EmpDataDump()



if __name__ == '__main__':
    Main()