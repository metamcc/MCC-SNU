import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class ProjClass:
    def __init__(self,projID,projName):
        self.projID = projID
        self.projName = projName
        self.importanceRate = 0
        self.num_EmpId  = 0
        self.G = nx.MultiGraph()
        self.empID_ContRate_Dict = {}
        self.date_EmpID_Dict= {}
        self.date_EdgeTuple= {}

    def getPeriods(self):
        return self.date_EmpID_Dict.keys()

    def getEmpId(self):
        return self.empID_ContRate_Dict.keys()

    def drawGraph(self):
        nx.draw(self.G)
        plt.show()

    def getContRateRanking(self):
        keyArray_CR =  np.array(list(self.empID_ContRate_Dict.keys()))
        valArray_CR =  np.array(list(self.empID_ContRate_Dict.values()))
        sortedIndex = valArray_CR.argsort()[::-1]
        rank_CR = list(keyArray_CR[sortedIndex])
        return  rank_CR

    def getCentralRanking(self):
        #choose centrality
        # closeness_centrality
        # degree_centrality

        keyArray_DC =  np.array(list(nx.degree_centrality(self.G).keys()))
        valArray_DC =  np.array(list(nx.degree_centrality(self.G).values()))
        #keyArray_DC =  np.array(list(nx.closeness_centrality(self.G).keys()))
        #valArray_DC =  np.array(list(nx.closeness_centrality(self.G).values()))
        sortedIndex = valArray_DC.argsort()[::-1]
        rank_DC = list(keyArray_DC[sortedIndex])
        return rank_DC

    def getDiscrepancyMeasure(self):
        retDict = {}
        rank_Centrality = self.getCentralRanking()
        rank_ContRate = self.getContRateRanking()

        for key in self.empID_ContRate_Dict.keys():
            rankContRate = rank_ContRate.index(key)
            rankCentrality = rank_Centrality.index(key)
            retDict[key] = (rankContRate - rankCentrality)/(len(rank_ContRate)- 1)

        return retDict

    def getProjImportance(self):
        return self.num_EmpId/34
