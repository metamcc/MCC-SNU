import  numpy as np

rootPath = '../../'


def main():
    creditRateDf = LoadData.loadCreditRateDataDataFrame()
    for col in creditRateDf.columns:
        creditRateDf[col] = (creditRateDf[col] - np.mean(creditRateDf[col]))/np.std(creditRateDf[col])
    creditRateDf['average'] = creditRateDf.mean(axis = 1)
    print(1)
if __name__ == '__main__':
    main()
