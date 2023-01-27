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

root_path = '../../'
quantile =7

def loadFeatureData():
    folder_path = root_path + 'Data/Features/'
    filename = folder_path + 'Discrepancy_Rate/discrepancy_rate.csv'
    df = pd.read_csv(filename)
    df = df.set_index('emp_id')
    return df




def main():
    resultList = []
    creditRateDf = LoadData.loadCreditRateDataDataFrame()
    feature_df = loadFeatureData()
    merged_df = pd.merge(creditRateDf, feature_df, left_index=True, right_index=True)

    X = np.array(list(merged_df.iloc[:,-1]))
    X_index = np.argsort(X)
    lenX = len(X)

    for column in creditRateDf.columns:
        print(column)

        Y = np.array(list(merged_df[column]))
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
        print(scipy.stats.spearmanr(X,Y))
        testResult = stats.ttest_ind(minQuantileY,maxQuantileY)
        print(testResult)
        plt.title('Quantile Analysis:' + column)
        plt.errorbar(quantX,quantCondExp_Y,decileSE_Y,fmt = 'rs--',elinewidth = 0.5,capsize = 5,capthick = 1,ecolor = 'b',label = '1 Standard Error')
        plt.grid()
        plt.xlabel('feature')
        plt.ylabel(column)
        plt.legend()

        plt.show()
        resultList.append(np.corrcoef(X,Y)[0][1])
    print(resultList)
if __name__ == '__main__':
    main()