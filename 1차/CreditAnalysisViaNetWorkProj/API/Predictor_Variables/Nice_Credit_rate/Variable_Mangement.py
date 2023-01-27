import  pandas as pd
import matplotlib.pylab as plt
import  numpy as np
import pickle
rootPath = '../../../'
quantile = 10

def loadNice_CreditRate_Data():
    inputDataPath = rootPath + 'Data/RawData/'
    filename= inputDataPath + 'NICE_CreditRate.csv'
    df = pd.read_csv(filename, engine='python')
    df = df.set_index('emp_id')
    return df

def average_Standardized_CreditRates(df):

    for col in df.columns:
        df[col] = (df[col] - np.mean(df[col]))/np.std(df[col])
    df['average'] = df.mean(axis = 1)
    return df

def quantile_rank(df):
    sorted_i_index = list(df.average.argsort())
    df['quantile_rank'] = np.nan
    obs = df.shape[0]
    for i in range(quantile):
        i_th_i_index  = sorted_i_index[int(obs*(i/quantile)):int(obs*((i+1)/quantile))]
        df.iloc[i_th_i_index, -1] = i
        #df.loc[i_th_i_index,:]
    return df


def main():
    creditData_df = loadNice_CreditRate_Data()
    df = average_Standardized_CreditRates(creditData_df)
    quantile_rank(df)


if __name__ == '__main__':
    main()
