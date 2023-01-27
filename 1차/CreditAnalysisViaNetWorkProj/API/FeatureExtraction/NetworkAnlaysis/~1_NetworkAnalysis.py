from scipy import stats
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import Library
import pickle
import platform
import scipy.stats

from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
    rc('font', family='AppleGothic')
elif platform.system() == 'Windows':
    path = "c:/Windows/Fonts/malgun.ttf"
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print('Unknown system... sorry~~~~')


quantile = 7
thresholdEmpNum = 6
variableList =['조직의 목표달성',	'수익성 지향','업무수행능력','	혁신/창의력','자기계발의지','판단력','책임감','협조성','소통','	위기대응' ]

def main():
    resultList = []
    capVarList = ['var1','var2','var3','var4','var5','var6','var7','var8','var9','var10']
    f = open('classDict.obj','rb')
    classDict = pickle.load(f)
    f.close()
    f = open('EvalCap_df.obj','rb')
    EvalCap_df = pickle.load(f)
    f.close()
    empDiscrepRate_Dict = {}


    for projKey in classDict.keys():
        if projKey == 12999901200:#휴가 제외
            continue
        if classDict[projKey].num_EmpId > thresholdEmpNum:
            dis_Measure = classDict[projKey].getDiscrepancyMeasure()
            proj_Importance = classDict[projKey].getProjImportance()
            for emp in dis_Measure.keys():
                if emp not in empDiscrepRate_Dict.keys():
                    empDiscrepRate_Dict[emp] = []
                #empDiscrepRate_Dict[emp].append(dis_Measure[emp]*proj_Importance)  #Assign Discrep. Measrue
                empDiscrepRate_Dict[emp].append(dis_Measure[emp])  #Assign Discrep. Measrue
    empList = list(set(list(EvalCap_df.index)).intersection(set(list(empDiscrepRate_Dict.keys()))))
    i = 0
    for capVar in capVarList:
        empId_DiscrepRate_EvalCap_df = pd.DataFrame([], columns=['emp_id','DiscrepRate','EvalCap'])
        for emp in empList:
            empId_DiscrepRate_EvalCap_df = empId_DiscrepRate_EvalCap_df.append({'emp_id': emp, 'DiscrepRate': np.average(empDiscrepRate_Dict[emp]), 'EvalCap':EvalCap_df.loc[emp][capVar] }, ignore_index=True)
        X = np.array(empId_DiscrepRate_EvalCap_df.DiscrepRate)
        X_index = np.argsort(X)
        lenX = len(X)
        Y = np.array(empId_DiscrepRate_EvalCap_df.EvalCap)
        Y = -(np.log(max(np.array(list(Y))) + 1 - np.array(list(Y))))
        quantX = []
        quantCondExp_Y = []
        decileSE_Y = []

        for j in range(quantile):
            j_th_indexY = X_index[int(lenX*(j/quantile)):int(lenX*((j+1)/quantile))]
            j_decileY = Y[j_th_indexY]
            if j == 0:
                minQuantileY = j_decileY
            elif j == (quantile - 1):
                maxQuantileY = j_decileY

            quantX.append(np.average(X[X_index[int(lenX*(j/quantile)):int(lenX*((j+1)/quantile))]]))
            quantCondExp_Y.append(np.average(j_decileY))
            decileSE_Y.append(np.std(j_decileY)/np.sqrt(len(j_decileY)))
        print(i)
        print(scipy.stats.wspearmanr(X,Y))
        testResult = stats.ttest_ind(minQuantileY,maxQuantileY)
        print(testResult)
        plt.title('Quantile Analysis:' + variableList[i])
        plt.errorbar(quantX,quantCondExp_Y,decileSE_Y,fmt = 'rs--',elinewidth = 0.5,capsize = 5,capthick = 1,ecolor = 'b',label = '1 Standard Error')
        plt.grid()
        plt.xlabel("Discrepancy Rate")
        plt.ylabel(variableList[i])
        plt.legend()
        plt.show()
        resultList.append(np.corrcoef(X,Y)[0][1])
        i += 1
    print(resultList)
if __name__ == '__main__':
    main()