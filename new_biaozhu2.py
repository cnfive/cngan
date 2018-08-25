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
  file1 = open(filepath)
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
  for line in file1:
      if len(line)>1:
   
         if "****************************" in line:
                
            seq=line.split("  ")
            tag=seq[0]
            if tag!="":
               paragrapha[tag]=para
            para=[]
                
         else:
            seq=line.split("        ")
           # print(line)
            sessionid=seq[0]
            line_num=seq[1]
            sentence=seq[3]

            para.append([sessionid,line_num,sentence])

            paragrapha[tag]=para

      #if sent_num>100000000:
       #     break

      sent_num+=1
  #print(paragrapha)
  #input()

  tag_list_dic={}
  key_list=[]
  line_count=0
  for s_tag in  paragrapha:
        
        #print(s_tag)
       # print(paragrapha[s_tag])
        for sess_line in paragrapha[s_tag]:

           # print(sess_line[0])
            #print(sess_line[1])
           # print(s_tag)
          #  tag_list.append([sess_line[0],sess_line[1],s_tag])   #[sessionid ,num,s_tag]
            key=(sess_line[0],sess_line[1])

            tag_list_dic[key]=s_tag
            key_list.append(key)
            line_count=line_count+1
            print(line_count)

  file1.close()
  #input()
  print("读取语料")
  filepath="./chat_new2.txt"
  file1 = open(filepath)


  pagecount=0
  for line in file1:

      #if len(line)>1 :
       pagecount=pagecount+1

  file1.close()
  file2 = open(filepath)
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
  page={}
  category={}

  j=0

  for line in file2:
   #i=i+1
   if len(line)>1:
     i=i+1

     line_split=line.split("	")
 
     s=line_split[3]
     session_id=line_split[0]
     user_tag=line_split[2]
     user_id=line_split[1]

     s_strip=s.strip()
  
     pattern = re.compile("ORDERID_\d+")
     out = re.sub(pattern, '订单号', s_strip)
     pattern2 = re.compile("\d+")
     out = re.sub(pattern2, '[数字x]', out)

     out=out.replace("&nbsp;","")
     out=out.replace("&quot","")

     if i==1:
        tag=line_split[0]
    

    
     if  tag == line_split[0]:
 
        para.append([user_id,user_tag,out])

     else:
        paragrapha[tag]=para

        para=[]

        j=0

        para.append([user_id,user_tag,out])


     tag=session_id
     print("i=",i)

     key=(session_id,str(j))

     category[key]=i-1

     page[i-1]=line

     j=j+1

     if i==pagecount:

          paragrapha[tag]=para

          para=[]

          break



       
       


  file2.close()

  f = open("chat_new4.txt", 'w')

  tag_line_list={}
  
  #input()
  num_list=[]
  for key in key_list:
      # print(key)
       tag=tag_list_dic[key]   #标签
       num=category[key]       #行数

       tag_line_list[num]=tag
       num_list.append(int(num))

  print(num_list)
  #input()
  num_list.sort()

  print(num_list)
 #input()
  for c in range(i):
       print(c)
       
       if c in num_list:
           tag=tag_line_list[c]
           line=page[c].strip()+"	"+tag+"\n"
       else:

           line=page[c].strip()+"\n"

       f.writelines(line)

  f.close()
   





if __name__ == '__main__':
    
       run_prediction()
       print("end")
