
# coding: utf-8

# In[ ]:


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

def eval_cos(A,B):


               list_a=[]  
               list_b=[]
               x_2=[]
               y_2=[]
               for x in A:
        
                          list_a.append(A[x])

                          x_2.append(A[x]**2)
      
               for y in B:

                          list_b.append(B[y])

                          y_2.append(B[y]**2)
     

               a=array(list_a)
               b=array(list_b)
               x2=array(x_2)
               y2=array(y_2)

               a_mul_b=a*b
               cos=a_mul_b.sum()/(math.sqrt(x2.sum())*math.sqrt(y2.sum()))
   
               return cos



def run_prediction(i):
  pcount=200*(i+1)-1
  
  f_tag=i
  f_num=0

  f_num=200*f_tag
	
  question_show={}


  print("读取语料")
  filepath="./chat_new2.txt"
  file = open(filepath)
  print("***********begin*************")
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

   if len(line)>1 and i>f_num:

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
 
     if  tag == line_split[0]:
 
        para.append([user_id,user_tag,out])

     else:
        paragrapha[tag]=para

        para=[]

        para.append([user_id,user_tag,out])


     tag=session_id

     if i>pcount:
          paragrapha[tag]=para
          para=[]
          break

  file.close()
#转换成id
  id_para={}
  count=0
  dic_list=[]
  dic_gobal=[]
  #print(paragrapha)
  for session in paragrapha:

       count=count+1
       dic={}

       id_list=[]
       s_and=""

       for key in paragrapha[session]:
       #      print(key)
             s=key[2]

             u_id=key[0]

             s_and=s_and+" "+s


             
       seg_list = jieba.cut(s_and)
       word_list=""
    #print(" ".join(seg_list))
       sentence=" ".join(seg_list)
       word=sentence.split(" ")  


       for w in word:
               if w not in dic:
                      dic[w]=1
               else:
                      dic[w]+=1
    
       del dic['']
    #   print(dic)
       if len(dic)>0:
              dic_list.append(dic)

       for w in dic:
              if w not in dic_gobal:

                    dic_gobal.append(w)

 
  num=0

  idf={}

  idf_list=[]


  print("##################################################")
  for w in dic_gobal:
     for d in dic_list:
          #print(d)
          if w not in d:
              if w not in idf:
                   idf[w]=0
          if w in d:
              if w not in idf:
                  idf[w]=1
              else:
                  idf[w]+=1
  

  print("**********************************")       
#print(idf)
  #input()
  print("读取停用词")
  filepath="./stopwords9.txt"
  file2 = open(filepath)

  stopword=[]
  for line in file2:
         stopword.append(line.strip())

  file2.close()

 # for word in stopword:
#     if word in idf:
     #    del idf[word]



  print("################计算tf-idf######################3")

  chat_group=[]

#count=0
  

#f = open("chat_tfdf2.txt", 'w')
  list_dic_tf_idf={}

  list_weight={}
  for session in paragrapha:

       #count=count+1
       dic={}
       #print("page count:"+str(count))
       id_list=[]
       s_and=""

       dic_tf_idf={}

       for w in dic_gobal:
            dic_tf_idf[w]=0   #初始化每段对话词典 词的tdidf 值为0

       list_sent_tfidf=[]

       list_sent_tfidf2=[]
       for key in paragrapha[session]:
     
             s=key[2]

             u_id=key[0]
   
             s_and=s_and+" "+s

       seg_list = jieba.cut(s_and)
       word_list=""
 
       sentence=" ".join(seg_list)
       word=sentence.split(" ")  


       for w in word:
               if w not in dic:
                      dic[w]=1
               else:
                      dic[w]+=1
                    #过滤停用词
       for word in stopword:
              if word in dic:
                    dic[word]=1
       del dic['']
       #print(dic)
       if len(dic)>0:
             d=dic
        #     print("*********************输出 d ***********************")
         #    print(d)


             total=0
             for v in d.values():
                 total=total+v
        #     print(total)

             tfidf_list=[]

      #print(d)
             weight_l=[]
             max_weight=0
             st_list=[]
             num=0
             
             list_sent_tfidf=[]
             list_sent_tfidf2=[]

             for key in paragrapha[session]:

               #     print("***********chat group*****************")
              #      print(key)
                    st=key[2]
                 #   print(st)

                    u_id=key[0]
                    u_tag=key[1]
         
             #       print("st=",st)
                    seg=jieba.cut(st)
                    sentence=" ".join(seg)

                    word=sentence.split(" ") 

           #del word['']
           #print("word:",word)
                    blank=''
                    while '' in word:
                           word.remove('')
           #print(word)
                    tfidf_list=[]
           #print(d)

                    for w in dic_gobal:
                           dic_tf_idf[w]=0   #初始化每段对话词典 词的tdidf 值为0                 

                    for key in word:
                        if key in idf:   #如果查询的词在 idf 词典里


                           tf=d[key]/total

                           tfidf=tf*math.log(count/idf[key])
                         #  tfidf=tf*(math.log((count+1)/(idf[key]+1)) +1)
                           tfidf_list.append(tfidf)
                           
                           #if u_tag!="1":

                           dic_tf_idf[key]=tfidf    #只比较用户提问的相似度

                    weight=0
                    for t in tfidf_list:
                           weight=weight+t

                    dic_tf_idf_copy=dic_tf_idf.copy()

                    list_sent_tfidf.append([dic_tf_idf_copy,u_tag])



             list_weight[session]=weight_l
        #     print(dic_tf_idf)
             list_dic_tf_idf[session]=list_sent_tfidf
    

  simliary={}

  c=0
  total_sess=[]


  print("计算相似度")
  

  simliay={}

  s_count=[]

  group={}
  temp_group=[]
  gobal_group=[]
  line_count=0
  for session in list_dic_tf_idf:
     print("#######################################################")

    

     num=0
     for sent_tfidf in list_dic_tf_idf[session]:
       if (session,num) not in gobal_group:

         A=sent_tfidf[0]


         temp_group=[]
         max_cos=0 # 计算最大相似度

         temp_group=[]
         for sess in list_dic_tf_idf:


            if session!=sess :
            
               num_c=0
             #max_num=0 # 句子位置
               for sent_tfidf_c in list_dic_tf_idf[sess]:
          
                  if (sess,num_c) not in gobal_group  and sent_tfidf[1] == sent_tfidf_c[1]:
          
                      B=sent_tfidf_c[0]
               
                      list_a=[]  
                      list_b=[]
                      x_2=[]
                      y_2=[]
                      for x in A:
            
                          list_a.append(A[x])
                    #x_2=x_2+A[x]*A[x]
                          x_2.append(A[x]**2)
       
                      for y in B:
                    #if y not  in stopword:
                          list_b.append(B[y])
                    #y_2=y_2+B[y]*B[y]
                          y_2.append(B[y]**2)
   
                      a=array(list_a)
                      b=array(list_b)
                      x2=array(x_2)
                      y2=array(y_2)

                      a_mul_b=a*b
                      cos=a_mul_b.sum()/(math.sqrt(x2.sum())*math.sqrt(y2.sum()))

                      if cos>0.8 :
                            print(sess)
                            print(" num_c_max_display:" ,num_c)

                            print("*************************")
                          #  print(session+"  and  "+ sess+"  cos:",cos)
                            print("*************************")
             
                            temp_group.append((sess,num_c) )
                            gobal_group.append((sess,num_c) ) 
                   # group[(session,num)]=(sess,num_c)   #找到最大相似度对话那一段
                  num_c=num_c+1

 

         group[(session,num)]=temp_group
  

       num=num+1   #每一句的序号

  
  del gobal_group
  del temp_group


#  f = open(output_file_path+"/result.txt", 'w')
  filename="./results/result_"+str(f_tag)+".txt"
  #input()
  f = open(filename, 'w')
  print("输出结果")
  r_count=0
  for key in group:
  
      key_txt=key[0]+"        "+str(key[1])


      answer=paragrapha[key[0]]
      txt=answer[key[1]]
   
      f.writelines("result_"+str(f_tag)+"_"+str(r_count)+"  "+txt[1]+"  "+"*************************************************************"+"\n")
      f.writelines(key_txt+"        "+txt[1]+"        "+txt[2]+"\n")
      for sent in group[key]:
        #    print(sent)
            sent_txt=sent[0]+"        "+str(sent[1])


            answer=paragrapha[sent[0]]
            txt=answer[sent[1]]
 
            f.writelines(sent_txt+"        "+txt[1]+"        "+txt[2]+"\n")

      r_count+=1
  f.close()     

                     
if __name__ == '__main__':

      filepath="./chat_new2.txt"
      file = open(filepath)

      ii=0


      for line in file:
             ii=ii+1
      print(ii)
      page=math.ceil(ii/200)
      print("page:",page)
      #input()
      for j in range(int(page)):
              run_prediction(j)
      print("end")




