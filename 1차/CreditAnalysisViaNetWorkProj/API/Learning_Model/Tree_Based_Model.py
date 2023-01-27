from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

root_path = '../../'
predictor_var  = 'CB'
result_rate_list = []
class Tree_Based_Model():
    def __init__(self):
        self.nLowestElts = 5
        self.nTestSample = 20
        self.features_df = self.loadFeatures()
        self.credit_rate_df = self.loadCreditRate()
        self.merged_df = pd.merge(self.features_df,self.credit_rate_df)
        self.train_df , self.test_df = self.split_sample(self.merged_df)
        self.train_regressor = self.train_model()
        self.model_evaluation()

    def loadFeatures(self):

        filename_discrep_rate = root_path + 'Data/Features/Discrepancy_Rate/discrepancy_rate.csv'
        filename_degree_cent= root_path + 'Data/Features/Centrality_Measures/degree_centrality.csv'
        filename_between_centrality= root_path + 'Data/Features/Centrality_Measures/between_centrality.csv'
        filename_info_cent= root_path + 'Data/Features/Centrality_Measures/info_centrality.csv'
        filename_ages= root_path + 'Data/Features/Raw_Features/ages.csv'

        df_discrep_rate = pd.read_csv(filename_discrep_rate)
        df_degree_cent = pd.read_csv(filename_degree_cent)
        feature_df = pd.merge(df_discrep_rate,df_degree_cent)
        df_info_cent = pd.read_csv(filename_info_cent)
        feature_df = pd.merge(feature_df,df_info_cent)
        df_between_centrality = pd.read_csv(filename_between_centrality)
        feature_df = pd.merge(feature_df,df_between_centrality)
        df_ages = pd.read_csv(filename_ages)
        feature_df = pd.merge(feature_df,df_ages)

        return feature_df

    def loadCreditRate(self):
        #filename = root_path + 'Data/Predictors/Nice_Credit_Rate/quantile_rank.csv'
        filename = root_path + 'Data/Predictors/Nice_Credit_Rate/'+predictor_var +'.csv'
        predictor_df = pd.read_csv(filename)
        return predictor_df

    def split_sample(self,df):
        nSample = df.shape[0]
        test_index = np.random.choice(nSample,self.nTestSample, replace=False)
        train_index = list(set(np.arange(nSample)).difference(set(test_index)))
        df_test = df.iloc[test_index,:]
        df_train = df.iloc[train_index,:]
        return df_train, df_test

    def train_model(self):
        nTrain = self.train_df.shape[0]
        X_train = self.train_df[['discrepancy_rate', 'degree_centrality', 'info_centrality','between_centrality','age' ]]
        y_train = np.array(list(self.train_df[predictor_var]))
        #masking = (y_train < 9) & (0 < y_train)
        #y_train[masking] = 5
        regr = RandomForestRegressor(n_estimators= 500, max_depth=2, random_state=0)
        regr.fit(X_train,y_train)
        return regr

    def model_evaluation(self):
        X_test = self.test_df[['discrepancy_rate', 'degree_centrality', 'info_centrality','between_centrality','age' ]]
        y_test = list(self.test_df[predictor_var])
        lowest_y_test = set(np.argsort(y_test)[-self.nLowestElts:])
        y_pred  = self.train_regressor.predict(X_test)
        lowest_y_pred = set(np.argsort(y_pred)[-self.nLowestElts:])
        result_rate_list.append(len(lowest_y_pred.intersection(lowest_y_test))/self.nLowestElts)


if __name__ == '__main__':
    for i in range(1000):
        Tree_Based_Model()
    print(np.average(np.array(result_rate_list)))
    print(np.std(np.array(result_rate_list))/np.sqrt(1000))
