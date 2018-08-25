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
  filepath="./results4/category_chat.txt"
  file = open(filepath)
  print("***********begin*************")
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
  for line in file:
      if len(line)>1:
   
         if "****************************" in line:
                
            seq=line.split("  ")
            tag=seq[0]
            if tag!="":
               paragrapha[tag]=para
            para=[]
                
         else:
            seq=line.split("        ")
            print(line)
            sessionid=seq[0]
            line_num=seq[1]
            sentence=seq[3]

            para.append([sessionid,line_num,sentence])

            paragrapha[tag]=para

      #if sent_num>100000000:
       #     break

      sent_num+=1

  tag_list=[]

  for s_tag in  paragrapha:
        
        #print(s_tag)
       # print(paragrapha[s_tag])
        for sess_line in paragrapha[s_tag]:

            print(sess_line[0])
            print(sess_line[1])
            print(s_tag)
            tag_list.append([sess_line[0],sess_line[1],s_tag])   #[sessionid ,num,s_tag]

  file.close()
 # input()
  print("读取语料")
  filepath="/media/hadoop/文档/simplechat-master/chat_new2.txt"
  file3 = open(filepath)
  pagecount=0
  for line in file3:
    if len(line)>1:
      pagecount+=1

  file3.close()

  file = open(filepath)
  print("***********现在开始计算*************")
  s_list=[]
  i=0
  sentence2=[]
  para=[]
  paragrapha={}
  all_sentence=[]

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
    #if "session_id" not in line:
     
     #if i>12821:
     #   break
     line_split=line.split("	")
     #print(line_split[6])
     s=line_split[3]
     session_id=line_split[0]
     user_tag=line_split[2]
     user_id=line_split[1]
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
 
        para.append([user_id,user_tag,out])

     else:
        paragrapha[tag]=para

        para=[]

        para.append([user_id,user_tag,out])


     tag=session_id
   #  print("i=",i)
    # i=i+1
     if i==pagecount:
          paragrapha[tag]=para
          para=[]
          break

  file.close()

  f = open("chat_new4.txt", 'w')
  for session in paragrapha:
         num=0
         print(session)
         for key in paragrapha[session]:

                #print(key)
                s=key[2]
    
                u_id=key[0]
                u_tag=key[1]
               # print(num)
                #print("***************************************************************")
                build_tag=""
                for c_tag in tag_list:
                   # build_tag=""
                   # print("session:",session)
                   # print("session1:",t_l[0])
                  #  print("num1:",num)
                  #  print("num2:",t_l[1])
                    if session==c_tag[0] and num==int(c_tag[1]) :

                   # if  num==t_l[1] :

                          print("*******--------------------------------------------********")
                          
                          print(c_tag[2])
                          build_tag=c_tag[2]
                         # continue

                f.writelines(session+"	"+u_id+"	"+u_tag+"	"+s+"	"+build_tag+"\n") 
                num=num+1
  f.close()
   





if __name__ == '__main__':
    
       run_prediction()
