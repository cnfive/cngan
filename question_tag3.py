import sys  
import jieba
import math
import numpy as np
from numpy import mat,matrix,array
import re
from operator import itemgetter, attrgetter

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


def run_prediction():
  question_show={}

  print("读取问题")
  filepath="../questions50.txt"

  #filepath=input_file_path
  file = open(filepath)
  question={}

  q_list=[]
  q_c=0
  for line in file:
   if len(line)>1:
     #print(line)
     sentence=[]
     line_split=line.split("<s>")

     #for s in  line_split:

           #if len(s)>0:
     sentence.append(line_split[0])
     sentence.append(line_split[1])
     sentence.append(line_split[2])
     sentence.append(line_split[3])
     sentence.append(line_split[4])

     k_q_c="question"+str(q_c)
     question[k_q_c]=sentence
     q_list.append(k_q_c)
     q_c=q_c+1

     #question_show[k_q_c]=sentence
     

  file.close()

#print(question)
  print("读取语料")
  filepath="../results4/category_chat.txt"
  file = open(filepath)
  print("***********现在开始计算*************")
  s_list=[]
  i=0
  sentence2=[]
  para=[]
  paragrapha={}
  all_sentence=[]
  

  sentence_order=[]
  sent_num=0
 


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
             print("............................................")
             print(key)
             s=key[2].strip()
             print(s)
           #  u_id=key[0]
           #  u_tag=key[1]

             
             
          
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
  print(dic_list)
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

  #for word in stopword:
    # if word in idf:
     #    del idf[word]



  print("################计算tf-idf######################3")

  chat_group=[]

#count=0
  file.close()

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
       #      print(key)
             s=key[2].strip()
    #print(s)
            # u_id=key[0]
            # u_tag=key[1]

             
             
          
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
                           print("tf:",tf)

                           tfidf=tf*math.log(count/idf[key])
                           print("tfidf:",tfidf)
 
                           tfidf_list.append(tfidf)
                           
                           #if u_tag!="1":

                           dic_tf_idf[key]=tfidf    #只比较用户提问的相似度

                    weight=0
                    for t in tfidf_list:
                           weight=weight+t
                    print("weight=",weight)
                    #input()

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

                   # f.writelines(session+"	"+u_id+"	"+u_tag+"	"+st+"	"+str(weight)+"	"+"\n")
#f.close()
#print(paragrapha)
  print(list_dic_tf_idf)
  print("*********************************************************")
  for  session in  list_dic_tf_idf:
         print(list_dic_tf_idf[session])

  #input()
  simliary={}

  c=0
  total_sess=[]




#计算question50 50 的tf-idf
  list_dic_tf_idf_question50={}



  for session in question:

        dic_tf_idf={}
        st=""

        max_weight=0

        dic={}
        u_tag=""

        list_sent_tfidf=[]
        for sent in question[session]:

               dic_tf_idf={}
               st=sent.strip()

               tfidf_list=[]

           #    print("st=",st)
               seg=jieba.cut(st)
               sentence=" ".join(seg)

               word=sentence.split(" ") 

           #del word['']
           #print("word:",word)
               blank=''
               while '' in word:
                     word.remove('')
           #print(word)
                   # tfidf_list=[]
           #print(d)
                    
               

               for w in  dic_gobal:
                     
                    dic_tf_idf[w]=0

           

               for w in word:
                    if w not in dic:
                          dic[w]=1
                    else:
                          dic[w]+=1
    
               for w in stopword:
                    if w in dic:
                               dic[w]=1               

               if len(dic)>0:
                     d=dic
               #      print("*********************输出 d ***********************")
                #     print(d)


                     total=0
                     for v in d.values():
                              total=total+v
               #      print("total:",total)

                     for key in word:
                     
                        if key in idf:   #如果查询的词在 idf 词典里
                           tf=d[key]/total
                         #  print("tf:",tf)
                           tfidf=tf*math.log(count/idf[key])
                         #  print("count:",count)
                         #  print("tf-idf:",tfidf)
 
                           tfidf_list.append(tfidf)

                           dic_tf_idf[key]=tfidf

                     weight=0
                     for t in tfidf_list:
                           weight=weight+t
                     print("weight=",weight)

 
                     weight_l.append([st,weight,u_tag])  #判断是否是客服回复

                     dic_tf_idf_copy=dic_tf_idf.copy()

                     list_sent_tfidf.append(dic_tf_idf_copy)
###################################################计算question 每句的tf-idf ######################################3





        list_dic_tf_idf_question50[session]=list_sent_tfidf  #5句对话 一个队列
        list_weight[session]=weight_l
  


#计算权重最大的语句相似度
  print("计算相似度")
  simliay={}

  s_count=[]
  #s_session=
  #group={}
  temp_group=[]
  gobal_group=[]
  line_count=0
  for session in list_dic_tf_idf_question50:
     print("#######################################################")

         #print(list_dic_tf_idf_question50[session])

     num=0
     for sent_tfidf in list_dic_tf_idf_question50[session]:

         print("line:",line_count)
         line_count+=1 

   # if "question"  in session :
         print(session)
         #print(list_dic_tf_idf[session])

         A=sent_tfidf

         group={}
        # print(A)

  
         max_cos=0 # 计算最大相似度
         max_num=-1
         temp_group=[]
         for sess in list_dic_tf_idf:

          #if sess not in total_sess:
           if "question" not in sess :

             num_c=0
             #max_num=0 # 句子位置
             for sent_tfidf_c in list_dic_tf_idf[sess]:

               

               B=sent_tfidf_c
               #print(B)
               list_a=[]  
               list_b=[]
               x_2=[]
               y_2=[]
               for x in A:
                    #print(A[x])
                    #检测x是不是停用词
                    #if x not in stopword:
                          list_a.append(A[x])
                    #x_2=x_2+A[x]*A[x]
                          x_2.append(A[x]**2)
                    #else:
                        #  list_a.append(0)
                         # x_2.append(0)
               for y in B:
                    #if y not  in stopword:
                          list_b.append(B[y])
                    #y_2=y_2+B[y]*B[y]
                          y_2.append(B[y]**2)
                    #else:
                     #     list_b.append(0)
                     #     y_2.append(0)

               a=array(list_a)
               b=array(list_b)
               x2=array(x_2)
               y2=array(y_2)

              # if sess[0]=="result_0_46":
                    # print("y2:",y2)

               a_mul_b=a*b
               cos=a_mul_b.sum()/(math.sqrt(x2.sum())*math.sqrt(y2.sum()))
             #  print("x2.sum():",x2.sum())
             #  print("y2.sum():",y2.sum())
               print(session+"  and  "+ sess[0]+"  cos:",cos)
             #  print(" 第几句:" ,num_c)
               if cos>0 :
                  if cos>max_cos:
                         max_cos=cos
                         print(" num_c_max_display:" ,num_c)
                         max_num=num_c
                         
                         group[cos]=sess    #找到最大相似度对话那一段
               num_c=num_c+1

      
           
         #group[session,num]=temp_group
         group_max=[]

         for  cos in group:
              if str(max_cos) in str(cos):
                     group_max=[group[cos]]  #cos 最大的那组对话
    

               
         simliary[session,num,max_num,max_cos]=group_max    #计算出每一句 最相似组,后面是语料位置

         num=num+1   #每一句的序号
 




     #input()
  filepath="./feature.txt"
  file2 = open(filepath)
  feature_dic={}

  for line in file2:
       seq=line.split("	")
       print(seq[0])
       print(seq[1])
       features=seq[1].strip().split("-")
       del features[0]
       print(features)
       feature_dic[seq[0].strip()]=features
       #for f in   features:
           



  s_count=0
  feature_tag=""
  feature_tag_list=[]

  for sim in  simliary:

       print("***********************************************")
       print("***********************************************")
       print("***********************************************")
       print(sim)

       print(simliary[sim])
    #   print( question[(sim[0])])
       q= question[(sim[0])]
       question_index=sim[1]
       answers_index=sim[2]
      # print("question_index:",question_index)

      # print("answers_index:",answers_index)

       print(".....................................原句............................................")
       print(q[question_index])

       print(".......................................最相似语句..........................................")
       print("相似度：",str(sim[3]))

       answer=""
       if simliary[sim]!=[]:
          # print(paragrapha[simliary[sim][0]])
           answer=paragrapha[simliary[sim][0]]
           

           print(answer)
           feature_tag+="-"+(simliary[sim][0])[0]

           feature_tag_list.append((simliary[sim][0])[0])

       s_count=s_count+1

       if s_count>4:
             s_count=0
             print(feature_tag)
             print(feature_tag_list)

             #查找 特征树

             feature_line=[]
             feature_line2=[]
             feature_line3=[]
             feature_line4=[]
             feature_line5=[]
             num=len(feature_tag_list)
          #if num==5:
             for key in feature_dic:
                #  print("test file")
                  if feature_tag_list[num-1] in feature_dic[key]:
                      # print("^^^^^^^^^^^^^^^^^^^^^^^^^^找到第一个特征^^^^^^^^^^^^^^^^^^^^^^^^^")                   
                     #  print(line)
                       feature_line.append(feature_dic[key])
                     #  print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

             for line2 in feature_line:
                  if feature_tag_list[2] in line2 or feature_tag_list[0] in line2:
                    #   print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^找到第二个特征^^^^^^^^^^^^^^^^^^^^^^^^^")    
                       feature_line2.append(line2)

                     #  print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^") 
   
             for line0 in feature_line2:
                  if feature_tag_list[3] in line0 or feature_tag_list[1] in line0:
                      # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^找到第三个特征^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")    
                       feature_line3.append(line0)
                     #  print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^") 

        

             if  feature_line3!=[]:
                   print("3+ features")
                   print(feature_line3)
             else:

                   if  feature_line2!=[]:
                         print("2+ features")
                         print(feature_line2)
                   else:

                         if  feature_line!=[]:
                               print("1 features")
                               print(feature_line)
                     
             file2.seek(0)
             feature_tag=""

             feature_tag_list=[]
             feature_line=[]
             feature_line2=[]
             feature_line3=[]
             feature_line4=[]
             feature_line5=[]

  file2.close()

  f = open("./result50.txt", 'w')
  print("输出结果")
  f.close()     
#根据权重计算3句问话中的核心问题    

  print("end!") 

if __name__ == '__main__':
    
       run_prediction()

