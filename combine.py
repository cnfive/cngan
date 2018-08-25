
#!/usr/bin/python3
# coding:UTF-8

import sys  
import jieba
import math
import numpy as np
from numpy import mat,matrix,array
import re
from operator import itemgetter, attrgetter
import pickle
import os
import copy 
import psutil


def  combine():
     rootdir="./results"
     file_list=[]
     for (dirpath, dirnames, filenames) in os.walk(rootdir):
		
             for filename in filenames:
                   if filename.endswith('.txt') :
                    filename_path = os.sep.join([dirpath, filename])
                    #print(filename_path)
                    file_list.append(filename_path)
    # print(file_list)

     length=len(file_list)
     j=0
     file_list=[]
     for n in range(700):
         filename_path =  rootdir+"/result_"+str(n)+".txt"
         file_list.append(filename_path)

     print(file_list)
    # input()
     length=len(file_list)

     f = open("category_chat.txt", 'w')
     for i in range(0,length,1):
       #j=j+1
       if j>=0  :
         print("****************************")
         f2=open(file_list[i])
         for line in f2:
             f.writelines(line)

         f2.close()
       j=j+1

     f.close()
                    
if __name__ == '__main__':




         combine()

         info = psutil.virtual_memory()
         print (u'内存使用：',psutil.Process(os.getpid()).memory_info().rss)
         print (u'总内存：',info.total)
         print (u'内存占比：',info.percent)
         print (u'cpu个数：',psutil.cpu_count())
   
         print("end")



