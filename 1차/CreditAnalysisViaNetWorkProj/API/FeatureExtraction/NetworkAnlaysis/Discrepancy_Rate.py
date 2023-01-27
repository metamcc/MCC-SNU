import Library.Classes as Classes
import codecs
import networkx as nx
import numpy as np
import pandas as pd
import pickle
rootPath = '../../../'

class calDiscrepancyRate():
    def __init__(self):
        self.thresholdEmpNum = 7
        self.inputDataPath = rootPath + 'Data/'
        self.inputDataPath1 = rootPath + 'Data/Variables/Whole/ProjAnalysis/'
        self.inputRawDataPath = rootPath + 'Data/RawData'
        self.mainDatadf = self.loadMainData()
        self.classDict = self.makeClassDict1()
        self.makeClassDict2()
        self.addGraphInfo()
        self.emp_DiscrepRate_Dict = self.calDiscrepancyRate()
        self.writeFile()
        self.saveBinaryFile()

    def loadMainData(self):
        #retDf = pd.DataFrame([],columns=['emp_id',	'dact_date',	'dact_star',	'prst_emp_id',
                                        # 'prst_tstar_cnt'])
        period = [2015,2016,2017]
        df_main = pd.DataFrame([],columns=['emp_id',	'emp_name',	'dact_date',	'dact_star',	'prst_emp_id',
                                           'emp_name1',	'prst_tstar_cnt'])
        for year in period:
            filename = self.inputRawDataPath + '/HR_DACT일일활동기록_' + str(year) + '.csv'
            df = pd.read_csv(filename,encoding='CP949')
            #df = pd.read_csv(filename,encoding='utf-8')
            df_main = pd.concat([df_main,df])

        masking = df_main['prst_emp_id'].isna()
        return df_main

    def makeClassDict1(self):
        retDict = {}
        filename = self.inputDataPath + 'Prj_List.csv'
        f = codecs.open(filename,'r')
        while True:
            line = f.readline()
            if not line: break
            data = line.rstrip(',\n').split(',')
            retDict[int(data[0])] = Classes.ProjClass(int(data[0]),data[1])
        f.close()

        filename = self.inputDataPath1 + 'Proj_Importance.csv'
        f = codecs.open(filename,'r')
        while True:
            line = f.readline()
            if not line: break
            data = line.rstrip('\n').split('|')
            data_tp= data[0].split(',')
            prj_Id = int(data_tp[0])
            importanceRate = float(data_tp[2])
            numId = int(data_tp[3])
            retDict[prj_Id].importanceRate = importanceRate
            retDict[prj_Id].num_EmpId = numId
            ID_ImpRateList = data[1].split(',')
            for lst in ID_ImpRateList:
                data_ttp = lst.split(':')
                emp_id = int(data_ttp[0])
                Cont_rate = float(data_ttp[1])
                retDict[prj_Id].empID_ContRate_Dict[emp_id] = Cont_rate

        filename = self.inputDataPath1 + 'Proj_Date_Participants.csv'
        f = open(filename,'r')
        while True:
            line = f.readline()
            if not line: break
            data = line.rstrip('\n').split(':')
            prj_id = int(data[0])
            data = data[1].split('&')
            for dt in data:
                dt = dt.split('|')
                date = int(dt[0])
                if not date in retDict[prj_id].date_EmpID_Dict.keys():
                    retDict[prj_id].date_EmpID_Dict[date] = []
                    retDict[prj_id].date_EdgeTuple[date] = []
                dt = dt[1].split(',')
                for d in dt:
                    retDict[prj_id].date_EmpID_Dict[date].append(int(d))

        return retDict

    def makeClassDict2(self):
        #edge info
        for key in self.classDict.keys():
            for key1 in self.classDict[key].date_EmpID_Dict.keys():
                emp_ID = self.classDict[key].date_EmpID_Dict[key1]
                masking = self.mainDatadf['dact_date'].isin([key1])
                data = self.mainDatadf[masking]
                masking1 = data['emp_id'].isin(emp_ID)
                masking2 = data['prst_emp_id'].isin(emp_ID)
                masking = masking1 & masking2
                data = data[masking]
                for index, row in data.iterrows():
                    self.classDict[key].date_EdgeTuple[key1].append((int(row['emp_id']) ,int(row['prst_emp_id'])))

        return self.classDict

    def addGraphInfo(self):
        for key in self.classDict.keys():
            self.classDict[key].G.add_nodes_from(list(self.classDict[key].empID_ContRate_Dict.keys()))
            for key1, value in self.classDict[key].date_EdgeTuple.items():
                self.classDict[key].G.add_edges_from(self.classDict[key].date_EdgeTuple[key1])

    def calDiscrepancyRate(self):
        emp_DiscrepRate_Dict = {}
        for projKey in self.classDict.keys():
            if projKey == 12999901200:#휴가 제외
                continue
            if self.classDict[projKey].num_EmpId >= self.thresholdEmpNum:
                dis_Measure = self.classDict[projKey].getDiscrepancyMeasure()
                proj_Importance = self.classDict[projKey].getProjImportance()
                for emp in dis_Measure.keys():
                    if emp not in emp_DiscrepRate_Dict.keys():
                        emp_DiscrepRate_Dict[emp] = []
                    emp_DiscrepRate_Dict[emp].append(dis_Measure[emp]*proj_Importance)  #Assign Discrep. Measrue
                    #emp_DiscrepRate_Dict[emp].append(dis_Measure[emp])  #Assign Discrep. Measrue
        return emp_DiscrepRate_Dict


    def writeFile(self):
        filename = rootPath + 'Data/Features/Discrepancy_Rate/discrepancy_rate.csv'
        f = open(filename,'w')
        f.write('emp_id,discrepancy_rate\n')
        for key, value in self.emp_DiscrepRate_Dict.items():
            f.write('%s,%s\n'%(key,np.mean(value)))
        f.close()



    def saveBinaryFile(self):
        f = open('classDict.obj','wb')
        pickle.dump(self.classDict,f)
        f.close()

def main():
    calDiscrepancyRate()

if __name__ =='__main__':
    main()