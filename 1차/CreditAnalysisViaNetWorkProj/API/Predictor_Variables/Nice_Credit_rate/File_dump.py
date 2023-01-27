import Predictor_Variables.Nice_Credit_rate.Variable_Mangement as Variable_Mangement


rootPath = '../../../'

def write_all_fields(df):

    for column in df.columns:
        filenamte = rootPath + 'Data/Predictors/Nice_Credit_Rate/'+ column +'.csv'
        f = open(filenamte,'w')
        f.write('emp_id,%s\n'%(column))

        for index, row in df.iterrows():
            f.write('%s,%s\n'%(index,row[column]))
        f.close()

def write_file_average_standardized_rate(df):
    filenamte = rootPath + 'Data/Predictors/Nice_Credit_Rate/average_standardized_rate.csv'
    f = open(filenamte,'w')
    f.write('emp_id,average_standardized_rate\n')

    for index, row in df.iterrows():
        f.write('%s,%s\n'%(index,row.average))

    f.close()

def write_file_quantile_rank(df):
    filenamte = rootPath + 'Data/Predictors/Nice_Credit_Rate/quantile_rank.csv'
    f = open(filenamte,'w')
    f.write('emp_id,quantile_rank\n')
    for index, row in df.iterrows():
        f.write('%s,%s\n'%(index,int(row.quantile_rank)))
    f.close()


def main():
    nice_credit_rate = Variable_Mangement.loadNice_CreditRate_Data()
    write_all_fields(nice_credit_rate)
    df = Variable_Mangement.average_Standardized_CreditRates(nice_credit_rate)
    df = Variable_Mangement.quantile_rank(df)
    write_file_average_standardized_rate(df)
    write_file_quantile_rank(df)





if __name__ == '__main__':
    main()