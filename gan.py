import tensorflow as tf
import re
import jieba
import numpy as np

from numpy import mat,matrix,array


filepath="./chat_new2.txt"

file_c = open(filepath)

pagecount=0

for line in file_c:
     pagecount+=1

file_c.close()


file = open(filepath)
print("***********现在开始计算*************")
para=[]
paragrapha={}
word_dic={}
i=1
ii=0
for line in file:

   ii=ii+1
   if len(line)>1:
     #line_split=line[56:]
  
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
     out=out.replace("&nbsp;","")
     out=out.replace("&quot","")  
    # print(out)
     seg_list = jieba.cut(out)
     word_list=""
    #print(" ".join(seg_list))
     sentence=" ".join(seg_list)
     word=sentence.split(" ") 
     for w in word:
        if w not in word_dic:
           word_dic[w]=i
           i=i+1

     if ii==1:
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
     if ii==pagecount:
          paragrapha[tag]=para
          para=[]
          break

          

file.close()

dic={}
i=1

#paragrapha={}

for session in   paragrapha:
     
     for  para_list  in paragrapha[session]:
         # for line in para_list:
             # print(para_list)
              sentence=para_list[2]
             # sentence_id=[]
              for s in sentence:
                 if s not in dic:
                     dic[s]=i
                     i=i+1
               
              
print(dic)

paragrapha2={}

for session in   paragrapha:
     parag=[]
     
     for  para_list  in paragrapha[session]:
              sentence=para_list[2]
              sentence_id=[]
              for s in sentence:
                    sentence_id.append(dic[s])

              parag.append(sentence_id)

     paragrapha2[session]=parag
              
print(paragrapha2)



input = tf.constant(1,shape=(64,10,1),dtype=tf.float32,name='input')#shape=(batch,in_width,in_channels)
w = tf.constant(3,shape=(3,1,32),dtype=tf.float32,name='w')#shape=(filter_width,in_channels,out_channels)
conv1 = tf.nn.conv1d(input,w,2,'VALID') #2为步长
print(conv1.shape)#宽度计算(width-kernel_size+1)/strides ,(10-3+1)/2=4  (64,4,32)
conv2 = tf.nn.conv1d(input,w,2,'SAME') #步长为2
print(conv2.shape)#宽度计算width/strides  10/2=5  (64,5,32)
conv3 = tf.nn.conv1d(input,w,1,'SAME') #步长为1
print(conv3.shape)  # (64,10,32)



