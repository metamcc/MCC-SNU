import  pandas as pd
import matplotlib.pylab as plt
import  numpy as np
import pickle
rootPath = '../../'

def loadCreditRateDataDataFrame():
    inputDataPath = rootPath + 'Data/RawData/'
    filename= inputDataPath + 'NICE_CreditRate.csv'
    df = pd.read_csv(filename, engine='python')
    df = df.set_index('emp_id')
    for col in df.columns:
        df[col] = (df[col] - np.mean(df[col]))/np.std(df[col])
    df['average'] = df.mean(axis = 1)
    return df

if __name__ == '__main__':
    print(1)
