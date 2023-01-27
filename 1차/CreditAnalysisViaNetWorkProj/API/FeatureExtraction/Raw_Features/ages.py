
import Library.Classes as Classes
import codecs
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import pickle

rootPath = '../../../'

now = 2015
def loadData():
    birthday_list = []
    filename = rootPath + 'Data/RawData/직원테이블.csv'
    f = open(filename,'r')
    f.readline()
    while True:
        line = f.readline()
        if not line: break
        data = line.rstrip('\n').split(',')
        birthday_list.append([int(data[0]),int(data[2][:-4])])
    f.close()
    return birthday_list
def writeData(birthday_list):
    filename = rootPath + 'Data/Features/Raw_Features/ages.csv'
    f = open(filename,'w')
    f.write('emp_id,age\n')
    for lst in birthday_list:
        age = now -lst[1]
        if age >= 20:
            f.write('%s,%s\n'%(lst[0],age ))
    f.close()




def main():
    birthday_list =  loadData()
    writeData(birthday_list)

if __name__ =='__main__':
    main()
