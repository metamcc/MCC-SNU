import platform
import scipy.stats
import networkx as nx
import matplotlib.pyplot as plt
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
import pickle
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr
from scipy import stats
Var = ' IC'

quantile =7
thresholdEmpNum = 6
variableList =['조직의 목표달성',	'수익성 지향','업무수행능력','	혁신/창의력','자기계발의지','판단력','책임감','협조성','소통','	위기대응' ]

def main():
    resultList = []
    capVarList = ['var1','var2','var3','var4','var5','var6','var7','var8','var9','var10']
    #f = open('classDict.obj','rb')
    classDf = pd.read_csv('Result_vector.csv')
    f = open('EvalCap_df.obj','rb')
    EvalCap_df = pickle.load(f)
    f.close()


    empList = list(set(list(EvalCap_df.index)).intersection(set(list(classDf['id']))))
    classDf.set_index(['id'],inplace=True)
    i = 0
    for capVar in capVarList:
        empId_DiscrepRate_EvalCap_df = pd.DataFrame([], columns=['emp_id','DiscrepRate','EvalCap'])
        for emp in empList:
            empId_DiscrepRate_EvalCap_df = empId_DiscrepRate_EvalCap_df.append({'emp_id': emp, 'DiscrepRate': classDf.loc[emp,Var], 'EvalCap':EvalCap_df.loc[emp][capVar] }, ignore_index=True)
        X = np.array(empId_DiscrepRate_EvalCap_df.DiscrepRate)
        X_index = np.argsort(X)
        lenX = len(X)
        Y = np.array(empId_DiscrepRate_EvalCap_df.EvalCap)
        #Y = -(np.log(max(np.array(list(Y))) + 1 - np.array(list(Y))))
        quantX = []
        quantCondExp_Y = []
        decileSE_Y = []

        for j in range(quantile):
            j_th_indexY = X_index[int(lenX*(j/quantile)):int(lenX*((j+1)/quantile))]
            #i_th_decileX = X[j_th_indexY]
            j_decileY = Y[j_th_indexY]
            if j == 3:
                minQuantileY = j_decileY
            elif j == (quantile - 1):
                maxQuantileY = j_decileY
            #plt.hist(i_th_decileX,5)
            #plt.show()

            quantX.append(np.average(X[X_index[int(lenX*(j/quantile)):int(lenX*((j+1)/quantile))]]))
            quantCondExp_Y.append(np.average(j_decileY))
            decileSE_Y.append(np.std(j_decileY)/np.sqrt(len(j_decileY)))
        print(i)
        print(scipy.stats.spearmanr(X,Y))
        testResult = stats.ttest_ind(minQuantileY,maxQuantileY)
        print(testResult)
        plt.title('Quantile Analysis:' + variableList[i])
        plt.errorbar(quantX,quantCondExp_Y,decileSE_Y,fmt = 'rs--',elinewidth = 0.5,capsize = 5,capthick = 1,ecolor = 'b',label = '1 Standard Error')
        plt.grid()
        plt.xlabel(Var)
        plt.ylabel(variableList[i])
        plt.legend()

        plt.show()
        resultList.append(np.corrcoef(X,Y)[0][1])
        i += 1
    print(resultList)
if __name__ == '__main__':
    main()