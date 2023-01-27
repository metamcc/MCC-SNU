
import Library.Classes as Classes
import codecs
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import pickle

rootPath = '../../../'



class CalCentraliyMeasure():
    def __init__(self):
        self.yearList = [2015,2016,2017]
        self.networkGraph = nx.Graph()
        self.makeNetworkGraph()
        self.calCentralityMeasure()
        self.writeFile()

    def loadFile(self, year):
        edge_list = []
        fileName = rootPath + 'Data/RawData/HR_DACT일일활동기록_' + str(year) +'.csv'
        f =  open(fileName,'r')
        line = f.readline()
        while True:
            line = f.readline()
            if not line: break
            data_list = line.rstrip('\n').split(',')
            if data_list[4]:
                sender = int(data_list[0])
                reciever = int(data_list[4])
                edge_list.append([sender,reciever])
        f.close()
        return edge_list

    def add_edges_NetworkGraph(self,edge_list):
        for edge in edge_list:
            self.networkGraph.add_edge(edge[0],edge[1])

    def makeNetworkGraph(self):
        for year in self.yearList:
            edge_list = self.loadFile(year)
            self.add_edges_NetworkGraph(edge_list)

    def calCentralityMeasure(self):
        self.degree_centrality = nx.degree_centrality(self.networkGraph)
        self.between_centrality = nx.betweenness_centrality(self.networkGraph)
        self.info_centrality = nx.current_flow_closeness_centrality(self.networkGraph)

    def writeFile(self):
        filename = rootPath + 'Data/Features/Centrality_Measures/degree_centrality.csv'
        f = open(filename,'w')
        f.write('emp_id,degree_centrality\n')
        for key, value in self.degree_centrality.items():
            f.write('%s,%s\n'% (key,value))
        f.close()

        filename = rootPath + 'Data/Features/Centrality_Measures/info_centrality.csv'
        f = open(filename,'w')
        f.write('emp_id,info_centrality\n')
        for key, value in self.info_centrality.items():
            f.write('%s,%s\n'% (key,value))
        f.close()

        filename = rootPath + 'Data/Features/Centrality_Measures/between_centrality.csv'
        f = open(filename,'w')
        f.write('emp_id,between_centrality\n')
        for key, value in self.between_centrality.items():
            f.write('%s,%s\n'% (key,value))
        f.close()

if __name__ =='__main__':
    CalCentraliyMeasure()
