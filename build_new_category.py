
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


def eval_cos(A,B):


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
   
               return cos



def run_prediction(filepath):
 
  f_tag="new1"

#print(question)
  print("读取语料")
  #filepath="/media/hadoop/文档/simplechat-master/result9.txt"
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
  tag="result_new_"
  u_tag=""
  for line in file1:
      if len(line)>1:
   
     
            seq=line.split("        ")
       #     print(line)
            sessionid=seq[0]
            line_num=seq[1]
            sentence=seq[3]
            u_line_tag=seq[2].strip()
            para.append([sessionid,line_num,sentence,u_line_tag])
            tag="result_new_"+str(sent_num)
            paragrapha[tag,u_line_tag]=para
            para=[]
      #if sent_num>50000:
          #  break

      sent_num+=1
  
  file1.close()
 
 
  #print(paragrapha)
#转换成id
  id_para={}
  count=0
  dic_list=[]
  dic_gobal=[]
  for session in paragrapha:

       count=count+1
       dic={}
      # print("page count:"+str(count))
       id_list=[]
       s_and=""

       for key in paragrapha[session]:
       #      print(key)
             s=key[2]
    #print(s)
             u_id=key[0]
             u_tag=key[1]

             
             
          
             #for sen in s:
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

 
 
   

  print("*****************1111111111111*****************") 
#print(dic_list)
  num=0

  idf={}

  idf_list=[]

#dic_gobal.remove('')
#dic_gobal.remove('')
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

  print("读取停用词")
  filepath="./stopwords9.txt"
  file2 = open(filepath)

  stopword=[]
  for line in file2:
         stopword.append(line.strip())

  file2.close()

 # for word in stopword:
   #  if word in idf:
    #     del idf[word]



  print("################计算tf-idf######################3")

  chat_group=[]

#count=0
 # file1.close()

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


       for key in paragrapha[session]:
        #     print("***********chat group*****************")
             print(session)
             s=key[2].strip()
             print(s)
             u_id=key[0]
             u_tag=key[1]

             
             
          
             #for sen in s:
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
    
       
       for w in stopword:
           if w in dic:
                  dic[w]=1
       del dic['']
       #print(dic)
       if len(dic)>0:
                    d=dic
  

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
 
                           tfidf_list.append(tfidf)
                           
                           #if u_tag!="1":

                           dic_tf_idf[key]=tfidf    #只比较用户提问的相似度

                    weight=0
                    for t in tfidf_list:
                           weight=weight+t
                  #  print("weight=",weight)
              #      print(dic_tf_idf)
                    dic_tf_idf_copy=dic_tf_idf.copy()

                   # del dic_tf_idf
                    list_sent_tfidf.append(dic_tf_idf_copy)
                    #if u_tag!="0":
                  #  if st not in st_list: 

                   #               st_list.append(st)
                    #              weight_l.append([st,weight,u_tag])  #判断是否是客服回复

            




           #  list_weight[session]=weight_l
        #     print(dic_tf_idf)
       list_dic_tf_idf[session]=list_sent_tfidf

        
 
                

  simliary={}

  c=0
  total_sess=[]



#计算权重最大的语句相似度
  print("计算相似度")

  simliay={}

  s_count=[]
  #s_session=
  group={}
  temp_group=[]
  gobal_group=[]
  for session in list_dic_tf_idf:
  
     #num=0

     if session not in gobal_group:
 
       for sent_tfidf in list_dic_tf_idf[session]:
       #if session not in gobal_group:
 
         A=sent_tfidf

         #group={}

         temp_group=[]
       #  max_cos=0 # 计算最大相似度
       #  max_num=-1
     #    print(num)
         temp_group=[]
         for sess in list_dic_tf_idf:

#            if sess not in gobal_group:
            if session[0]!=sess[0] and session[1] == sess[1]:
                if sess not in gobal_group:
                    #num_c=0
  
                    for sent_tfidf_c in list_dic_tf_idf[sess]:

                      #  if  session[1] == sess[1]:

                           B=sent_tfidf_c
             #  print(B)
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
                        #   print(session+"  and  "+ sess+"  cos:",cos)

                           if cos==1 :
                                # print(sess)
                                 print(" num_c_max_display:" ,sess)

                                 temp_group.append(sess)
                
                                 gobal_group.append(sess) 
             
                   # num_c=num_c+1


         group[session]=temp_group
         #simliary[session,num,max_num,max_cos]=group_max    #计算出每一句 最相似组,后面是语料位置

         #num=num+1   #每一句的序号
       #  c=c+1






  del gobal_group
  del temp_group


#  f = open(output_file_path+"/result.txt", 'w')
  filename="./result_"+str(f_tag)+".txt"

  f = open(filename, 'w')
 # print("输出结果")
  r_count=0

  for key in group:


      answer=paragrapha[key]
      #print(answer)
      #input()
      #txt=answer[0]
      u_tag=key[1]

      #print(txt[2])
      f.writelines("result_"+str(f_tag)+"_"+str(r_count)+"  "+u_tag+"  "+"**********************************************************"+"\n")

      for txt in answer:
      #txt=answer[0]
            txt_line=txt[0]+"        "+txt[1]+"        "+txt[3]+"        "+txt[2].strip()
      #txt_line=txt_line+"\n"
            f.writelines(txt_line+"\n")

      for sent in group[key]:
    
            answer=paragrapha[sent]
          #  txt=answer[sent[1]]
          #  print(txt[2])
           
            for txt2 in answer:
                    txt_line2=txt2[0]+"        "+txt2[1]+"        "+txt2[3]+"        "+txt2[2].strip()
                    f.writelines(txt_line2+"\n")

      r_count+=1
  f.close()     
    

 # print("end!") 
                     
                     
if __name__ == '__main__':

     #rootdir="./results"
         file1="./new_results_2.txt"
  


         run_prediction(file1)
 
 

         info = psutil.virtual_memory()
         print (u'内存使用：',psutil.Process(os.getpid()).memory_info().rss)
         print (u'总内存：',info.total)
         print (u'内存占比：',info.percent)
         print (u'cpu个数：',psutil.cpu_count())
     
         print("end")



