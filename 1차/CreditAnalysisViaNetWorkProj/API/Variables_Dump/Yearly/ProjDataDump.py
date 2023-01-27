import  pandas as pd
import  numpy as np

rootPath = '../../../'

class ProjDataDump():
    def __init__(self,Year):
        self.Year = Year
        self.inputDataPath = rootPath + 'Data/RawData'
        self.inputDataPath2 = rootPath + 'Data'
        self.prj_id_name_dict = self.make_prj_id_name_dict()
        self.outputDataPath = rootPath + 'Data/Variables/Yearly/ProjAnalysis'
        self.mainDataList = self.loadData()
        self.fileDump()

    def make_prj_id_name_dict(self):
        retDict = {}
        filename = self.inputDataPath2 + '/Prj_List.csv'
        f = open(filename,'r')
        while True:
            line = f.readline()
            if not line: break
            data = line.rstrip('\n').split(',')
            retDict[data[0]] = data[1]
        return retDict

    def loadData(self):
        retList = []
        tpRetListContainer = []
        proj_pact_rate_List = []

        filename = self.inputDataPath + '/HR_pace 프로젝트 참여도_' + str(self.Year) + '.csv'
        df = pd.read_csv(filename)
        unique_proj_id = sorted(list(df.prj_id.unique()))
        dateTotal = np.array(df.dact_date.unique())

        for prj_id in unique_proj_id:
            i_th_prj_list = [] # prj_id, num_id, sum_pact_rate, ...
            tpContainerList = []
            emp_pact_rate_List = []

            i_th_prj_list.append(prj_id)
            i_prj_df = df[df.prj_id == prj_id ]
            i_prj_df.loc[:,'pact_rate'] = np.array(i_prj_df.pact_rate/100)
            prj_id_date = i_prj_df.dact_date.unique()
            #weigtht = len(prj_id_date)/len(dateTotal)
            i_th_prj_list.append(len(i_prj_df.emp_id.unique()))
            sum_pact_rate = sum(i_prj_df.pact_rate)
            i_th_prj_list.append(sum_pact_rate)
            proj_pact_rate_List.append(sum_pact_rate)

            IDunique = sorted(i_prj_df.emp_id.unique())
            for ID in IDunique:
                lisTtp = []
                lisTtp.append(ID)
                i_th_prj_j_th_emp_df = i_prj_df[i_prj_df.emp_id == ID]
                sum_j_th_emp_normalized_pact_rate = sum(i_th_prj_j_th_emp_df.pact_rate)
                lisTtp.append(sum_j_th_emp_normalized_pact_rate)
                emp_pact_rate_List.append(sum_j_th_emp_normalized_pact_rate)
                tpContainerList.append(lisTtp)
            sortedIndex = np.argsort(emp_pact_rate_List)
            sortedIndex = sortedIndex[::-1]
            for index in sortedIndex:
                i_th_prj_list.append(tpContainerList[index])
            tpRetListContainer.append(i_th_prj_list)
        sortedIndex = np.argsort(proj_pact_rate_List)
        sortedIndex =sortedIndex[::-1]
        for index in sortedIndex:
            retList.append(tpRetListContainer[index])
        return retList

    def fileDump(self):
        filename = self.outputDataPath + '/ProjAnalysis_' + str(self.Year) + '.csv'
        f = open(filename,'w')
        for Data in self.mainDataList:
            prj_Id = Data.pop(0)
            prj_name = self.prj_id_name_dict[str(prj_Id)]
            num_emp = Data.pop(0)
            sum_pact_rate = Data.pop(0)
            f.write('%s,%s,%s,%s|'%(prj_Id,prj_name,sum_pact_rate,num_emp))
            i = 1
            for data in Data:
                f.write('%s:%s'%( data[0],data[1]))
                if not (i == len(Data)):
                    f.write(',')
                else:
                    f.write('\n')
                i += 1
        f.close()
def Main():
    period = [2015,2016,2017]
    for year in period:
        instance = ProjDataDump(year)



if __name__ == '__main__':
    Main()