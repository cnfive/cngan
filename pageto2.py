
# coding: utf-8

# In[ ]:


import sys  
import jieba
import math
import numpy as np
from numpy import mat,matrix,array
import re
from operator import itemgetter, attrgetter
import os
import psutil





def run_prediction(f_tag,filepath):
 


#print(question)
  print("读取语料")
  #filepath="/media/hadoop/文档/simplechat-master/result9.txt"
  file = open(filepath)
  print("***********现在开始计算*************")
  s_list=[]
  i=0
  sentence2=[]
  para=[]
  paragrapha={}
  all_sentence=[]
  #tag="result0"
  sent_num=0
  sentence_order=[]
  tag=""
  u_tag=""
  for line in file:
      if len(line)>1:
   
         if "****************************" in line:
                
            seq=line.split("  ")
            tag=seq[0]
            u_tag=seq[1]

            if tag!="":
               paragrapha[tag,u_tag]=para
            para=[]
                
         else:
            seq=line.split("        ")
       #     print(line)
            sessionid=seq[0]
            line_num=seq[1]
            sentence=seq[3]
            u_line_tag=seq[2].strip()
            para.append([sessionid,line_num,sentence,u_line_tag])

            paragrapha[tag,u_tag]=para

      #if sent_num>50000:
          #  break

      #sent_num+=1
  
  file.close()
 
#转换成id

  filename="./results2_0/result_"+str(f_tag)+".txt"

  f = open(filename, 'w')

  r_count=0
  for session in paragrapha:



       print(session)
       u_tag=session[1]
       if u_tag=="0":
            f.writelines("result_"+str(f_tag)+"_"+str(r_count)+"  "+u_tag+"  "+"******************************************************"+"\n")

            for key in paragrapha[session]:
                  print(key)

                  txt_line=key[0]+"        "+key[1]+"        "+key[3]+"        "+key[2].strip()
             
                  f.writelines(txt_line+"\n")

            r_count+=1
 
  f.close() 
   

  filename2="./results2_1/result_"+str(f_tag)+".txt"

  f = open(filename2, 'w')

  r_count=0
  for session in paragrapha:



       print(session)
       u_tag=session[1]
       if u_tag=="1":
            f.writelines("result_"+str(f_tag)+"_"+str(r_count)+"  "+u_tag+"  "+"******************************************************"+"\n")

            for key in paragrapha[session]:
                  print(key)

                  txt_line=key[0]+"        "+key[1]+"        "+key[3]+"        "+key[2].strip()
             
                  f.writelines(txt_line+"\n")

            r_count+=1
 
  f.close() 



    

 # print("end!") 
                     
                     
if __name__ == '__main__':

     rootdir="./results"
     file_list=[]
     for (dirpath, dirnames, filenames) in os.walk(rootdir):
		
             for filename in filenames:
                   if filename.endswith('.txt') :
                    filename_path = os.sep.join([dirpath, filename])
                    #print(filename_path)
                    file_list.append(filename_path)
     print(file_list)

     length=len(file_list)
     j=0
     file_list=[]
     for n in range(20):
         filename_path =  rootdir+"/result_"+str(n)+".txt"
         file_list.append(filename_path)

     print(file_list)
    # input()
     length=len(file_list)



     for i in range(0,length,1):
       #j=j+1
       if j>=0  and j<9:
         print("****************************")
         filepath=file_list[i]
    
         #j=j+1
         run_prediction(j,filepath)
         print(j)
 

       j=j+1
     print("end")



