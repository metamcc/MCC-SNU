import platform
from Library import LoadData
import scipy.stats
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
import pandas as pd
import numpy as np
from scipy import stats
Var = ' degree'

quantile =7
thresholdEmpNum = 6

def main():
    resultList = []
    creditRateDf = LoadData.loadCreditRateDataDataFrame()
    creditVarList = ['average','CB', 'SP', 'PI', 'CP', 'DEP', 'ML']
    #f = open('classDict.obj','rb')
    classDf = pd.read_csv('Result_vector.csv')


    empList = list(set(list(creditRateDf.index)).intersection(set(list(classDf['id']))))
    classDf.set_index(['id'],inplace=True)
    i = 0
    for creditVar in creditVarList:
        print(creditVar)
        empId_DiscrepRate_Credit_Rate = pd.DataFrame([], columns=['emp_id','DiscrepRate','Credit_Rate'])
        for emp in empList:
            empId_DiscrepRate_Credit_Rate = empId_DiscrepRate_Credit_Rate.append({'emp_id': emp, 'DiscrepRate': classDf.loc[emp,Var], 'Credit_Rate':creditRateDf.loc[emp][creditVar] }, ignore_index=True)
        X = np.array(list(empId_DiscrepRate_Credit_Rate.DiscrepRate))
        X_index = np.argsort(X)
        lenX = len(X)
        Y = np.array(list(empId_DiscrepRate_Credit_Rate.Credit_Rate))
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
        print(scipy.stats.spearmanr(X,Y))
        testResult = stats.ttest_ind(minQuantileY,maxQuantileY)
        print(testResult)
        plt.title('Quantile Analysis:' + creditVarList[i])
        plt.errorbar(quantX,quantCondExp_Y,decileSE_Y,fmt = 'rs--',elinewidth = 0.5,capsize = 5,capthick = 1,ecolor = 'b',label = '1 Standard Error')
        plt.grid()
        plt.xlabel(Var)
        plt.ylabel(creditVarList[i])
        plt.legend()

        plt.show()
        resultList.append(np.corrcoef(X,Y)[0][1])
        i += 1
    print(resultList)
if __name__ == '__main__':
    main()