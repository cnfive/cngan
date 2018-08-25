import sys  
import jieba
import math
import numpy as np
from numpy import mat,matrix,array
import re
from operator import itemgetter, attrgetter




def run_prediction():
  question_show={}

  print("读取问题")


#print(question)
  print("读取语料")
  filepath="./result_16000_1.txt"
  file1 = open(filepath)
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
  for line in file1:
      if len(line)>1:
   
         if "****************************" in line:
                
            seq=line.split("  ")
            tag=(seq[0],seq[1])
            if tag!="":
               paragrapha[tag]=para
            para=[]
                
         else:
            seq=line.split("        ")
            print(line)
            sessionid=seq[0]
            line_num=seq[1]
            sentence=seq[3]
            chat_tag=seq[2]

            para.append([sessionid,line_num,chat_tag,sentence])

            paragrapha[tag]=para

      if sent_num>100000000:
            break

      sent_num+=1

  tag_list=[]
  q_string_0="&nbsp;"
  q_string_1="https://item.jd.com/[数字x].html"
  q_string_2="订单金额:[金额x]，下单时间:"
  q_string_3="马上核实情况，请您稍等哈#E-s[数字x]"

  q_string_result_id_0=[]
  q_string_result_id_1=[]
  q_string_result_id_2=[]
  q_string_result_id_total=[]
  for s_tag in  paragrapha:
        
        #print(s_tag)
       # print(paragrapha[s_tag])
        for sess_line in paragrapha[s_tag]:

         #   print(sess_line[0])
         #   print(sess_line[1])
         #   print(s_tag)
         #   print(sess_line[2])
       #     tag_list.append([sess_line[0],sess_line[1],s_tag])   
            
            if  q_string_0 in sess_line[3]:
                  #  print(s_tag)
                 #   print(sess_line[2])
                    if s_tag not in q_string_result_id_0:
                           
                           q_string_result_id_0.append(s_tag)


            if  q_string_1 in sess_line[3]:
                  #  print(s_tag)
                  #  print(sess_line[2])
                    if s_tag not in q_string_result_id_1:
                           
                           q_string_result_id_1.append(s_tag)

            if  q_string_2 in sess_line[3]:
                    print(s_tag)
                    print(sess_line[3])
                    if s_tag not in q_string_result_id_2:
                           
                           q_string_result_id_2.append(s_tag)

  print(q_string_result_id_0)

  print(q_string_result_id_1)

  print(q_string_result_id_2)

  for result_id in  q_string_result_id_0:
     if  result_id not in  q_string_result_id_total:
        q_string_result_id_total.append(result_id)

  for result_id in  q_string_result_id_1:
     if  result_id not in  q_string_result_id_total:
        q_string_result_id_total.append(result_id)

  for result_id in  q_string_result_id_2:
     if  result_id not in  q_string_result_id_total:
        q_string_result_id_total.append(result_id)

  print(q_string_result_id_total)

  f = open("new_results.txt", 'w')
  f2 = open("new_results_2.txt", 'w')
  for s_tag in  paragrapha:
    if s_tag not in   q_string_result_id_total:

       f.writelines(s_tag[0]+"  "+s_tag[1]+"  "+"*******************************************************************"+"\n")
 
       for sess_line in paragrapha[s_tag]:

             txt_line=sess_line[0]+"        "+sess_line[1]+"        "+sess_line[2]+"        "+sess_line[3].strip()
             f.writelines(txt_line+"\n")
    else:
       
       f2.writelines(s_tag[0]+"  "+s_tag[1]+"  "+"*******************************************************************"+"\n")
 
       for sess_line in paragrapha[s_tag]:

             txt_line=sess_line[0]+"        "+sess_line[1]+"        "+sess_line[2]+"        "+sess_line[3].replace("&nbsp;","").strip()
             f2.writelines(txt_line+"\n")

  f2.close()
  f.close()
  file1.close()

if __name__ == '__main__':
    
       run_prediction()
