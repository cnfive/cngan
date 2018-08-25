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
  filepath="./chat_new4.txt"
  file = open(filepath)
  print("***********现在开始计算*************")
  s_list=[]
  i=0
  sentence2=[]
  para=[]
  paragrapha={}
  all_sentence=[]
  tag=""

  sentence_order=[]

  tag=""
  #first_tag=""
  sentence_order=[]
  for line in file:

   #i=i+1

   i=i+1
  # if i>pcount:
     #   break
   if len(line)>1 :
     #line_split=line[56:]
    if "session_id" not in line:
     
     #if i>12821:
     #   break
     line_split=line.split("	")
     #print(line_split[6])
     s=line_split[3]
     session_id=line_split[0]
     user_tag=line_split[2]
     user_id=line_split[1]
    # txt_tag=line_split[4]

     txt_tag="nofeature"
        
     if len(line_split)==5:
        
        
          txt_tag=line_split[4]
     #user_tag=line_split[2]
     #user_tag=int(user_tag)+1
     s_strip=s.strip()
     #s_strip=s_strip.replace("","")
     pattern = re.compile("ORDERID_\d+")
     out = re.sub(pattern, '订单号', s_strip)
     pattern2 = re.compile("\d+")
     out = re.sub(pattern2, '[数字x]', out)
     if i==1:
        tag=line_split[0]
     #tag = line_split[0]

    
     if  tag == line_split[0]:
 
        para.append([user_id,user_tag,out,txt_tag])

     else:
        paragrapha[tag]=para

        para=[]

        para.append([user_id,user_tag,out,txt_tag])


     tag=session_id
   #  print("i=",i)
    # i=i+1
     if i>2000000:
          paragrapha[tag]=para
          para=[]
          break

  file.close()





#转换成id
 
  count=0
  feature_dic={}

  for session in paragrapha:

       count=count+1
   
       feature_string=""
       for key in paragrapha[session]:
       #      print(key)
             s=key[2]
    #print(s)
             u_id=key[0]
             u_tag=key[1]

             
             t_tag=key[3].strip()
             feature_string=feature_string+"-"+t_tag

       feature_dic[session]=feature_string
#count=0
  file.close()


             
 

#过滤停用词





#  f = open(output_file_path+"/result.txt", 'w')
  f = open("./feature.txt", 'w')
  print("输出结果")
  for sess in   feature_dic:
        print(sess)
        print(feature_dic[sess])
             
        f.writelines(sess+"	"+feature_dic[sess]+"\n") 
  f.close()     
#根据权重计算3句问话中的核心问题    

  print("end!") 
                     
                     
if __name__ == '__main__':
    
       run_prediction()




