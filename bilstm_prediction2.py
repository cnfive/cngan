import tensorflow as tf
import re
import jieba
import numpy as np

from numpy import mat,matrix,array


filepath="./feature.txt"

f=open(filepath,"r")

i=1
chat_list=[]
dic={}
for line in f:
  #if len(line)>1:
    #print(line)
    line_seq=line.strip().split("	")
    word_seq=line_seq[1].split("-")
   # print(type(word_seq))
    word_seq2=[]
   # word_seq2=word_seq



    for word in  word_seq:
           # print(i)
            if word not in dic:
               # if word!='':
                    dic[word]=i

                    i=i+1

            if word!='':
               word_seq2.append(word)
   # print(word_seq2)
    chat_list.append(word_seq2)

f.close()
#senten to id
max_i=i                 #归一化 最大值，最小值是1
chat_sentence_id_list=[]
#print(dic)

for session in chat_list:
    sentence_to_id=[]
    for sentence in session :
         sentence_to_id.append(dic[sentence])
        # norm=(dic[sentence]-1)/(max_i-1)      #归一化
         sentence_to_id.append(dic[sentence])


    chat_sentence_id_list.append(sentence_to_id)

#print(chat_sentence_id_list)
#print(len(dic))
x=[]
y=[]

count_x=0
for session in  chat_sentence_id_list:
     if len(session)>=6:
         #print(session)
         step=len(session)-5
         for i in range(step):
           # norm=(session[5+i]-1)/(max_i-1)      #归一化    
            norm=[]
            for value in   session[0+i:5+i]:  
                 normliztion=(value-1)/(max_i-1)
                 norm.append(normliztion)
            count_x+=1  
            x.append(norm)

            y.append(session[5+i])
            if count_x>500:
                 break

#print(y)
#input()
#print(x)
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


print("读取语料")
filepath="./results4/category_chat.txt"
file1 = open(filepath)
print("***********现在开始计算*************")
s_list=[]
 
sentence2=[]
para=[]
paragrapha2={}
all_sentence=[]
  #tag="result0"
sent_num=0
sentence_order=[]
tag=""
u_tag=""

for line in file1:
      if len(line)>1:
   
         if "****************************" in line:
                
            seq=line.split("  ")
            tag=seq[0]
            u_tag=seq[1]

            if tag!="":
               paragrapha2[tag]=para
            para=[]
                
         else:
            seq=line.split("        ")
       #     print(line)
            sessionid=seq[0]
            line_num=seq[1]
            sentence=seq[3]
            u_line_tag=seq[2].strip()
            para.append([sessionid,line_num,sentence,u_line_tag])

            paragrapha2[tag]=para

      #if sent_num>50000:
          #  break

      #sent_num+=1
  
file1.close()
#print(len(x))
#print(y)
#input()

y_t=[]

count_1=0
for label in y:

     count_1+=1
     fe=""
     for feature in dic:
         if label==dic[feature]:
             #print(feature)
             fe=feature
     
     list_sentence=paragrapha2[fe]
     txt=list_sentence
     sentence=(txt[0])[2]
     #print(sentence)
   # print(fe)

     seg_list = jieba.cut(sentence.strip())
     word_list=""
    #print(" ".join(seg_list))
     sentence=" ".join(seg_list)
     word=sentence.split(" ")
     sentence_to_id=[]
     sentence_to_id.append(0)
     count=0
     for w  in word:
         count+=1
         sentence_to_id.append(word_dic[w])
         if count==18:
             break
     length=len(sentence_to_id)  #限制序列长度为20

     if length<19:
         for i in range(19-length):

             sentence_to_id.append(0)   #补0
         
     sentence_to_id.append(0)

     y_t.append(sentence_to_id)

     if count_1>500:
          break

#print(y_t)

learning_rate=0.01

global_step = tf.Variable(-1, trainable=False, name='global_step')






num_layer=8

num_units=160

y_label=tf.placeholder(dtype=tf.float32, shape=[None,20])

#shu chu fen lei shu mu
category_num=len(word_dic)
#print(word_dic)
print("category_num:",category_num)

batch_size=10
n_steps=1
x_input=tf.placeholder(dtype=tf.float32, shape=[None,n_steps,5])
keep_prob = tf.placeholder(tf.float32, [])



def weight(shape, stddev=0.1, mean=0):
    initial = tf.truncated_normal(shape=shape, mean=mean, stddev=stddev)
    return tf.Variable(initial)


def bias(shape, value=0.1):
    initial = tf.constant(value=value, shape=shape)
    return tf.Variable(initial)


def lstm_cell(num_units, keep_prob=0.5):
    cell = tf.nn.rnn_cell.LSTMCell(num_units, reuse=tf.AUTO_REUSE)
    return tf.nn.rnn_cell.DropoutWrapper(cell, output_keep_prob=keep_prob)


keep_prob=0.1

    
  
cell_fw = [lstm_cell(num_units, keep_prob) for _ in range(num_layer)]
cell_bw = [lstm_cell(num_units, keep_prob) for _ in range(num_layer)]



#x_input=[1.2910222314028247e-05, 1.2910222314028247e-05, 2.5820444628056494e-05, 2.5820444628056494e-05, 3.873066694208474e-05]
#x_input=tf.expand_dims(x_input,0) 
#x_input=tf.expand_dims(x_input,0)

#n_steps=1
#x_inputs=[1,1,x[i]]
print(x_input)
inputs = tf.unstack(x_input, n_steps, axis=1)
output, _, _ = tf.contrib.rnn.stack_bidirectional_rnn(cell_fw, cell_bw, inputs, dtype=tf.float32)
print(len(output))
print(output)
output = tf.stack(output, axis=1)
print("+++++++++++++++++++++++++++")
print('Output:', output)


sentence_length=20
output = tf.reshape(output, [sentence_length, -1])
#output = tf.reshape(output, [-1, num_units * 2])
# [-1, FLAGS.num_units * 2]
print('Output Reshape', output)




# Output Layer
with tf.variable_scope('outputs'):

     #   w = weight([FLAGS.num_units * 2, FLAGS.category_num])
     #   b = bias([FLAGS.category_num])
     #   y = tf.matmul(output, w) + b
     w = weight([16, category_num])
     b = bias([category_num])
     y2 = tf.matmul(output, w) + b
     print("w:",w)
     print("b:",b)
     print("y.shape:",y2.shape)

        
     y_predict = tf.cast(tf.argmax(y2, axis=1), tf.int32)
     print('Output Y shape:', y_predict.shape)
       



#对输出标签 定义为1行多列
y_label_reshape = tf.cast(tf.reshape(y_label, [-1]), tf.int32)
print('Y Label Reshape', y_label_reshape)
print("y_predict.shape:",y_predict.shape)
print("y_label.shape",y_label.shape)
    

    
    # Prediction
correct_prediction = tf.equal(y_predict, y_label_reshape)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
tf.summary.scalar('accuracy', accuracy)
    
print('Prediction', correct_prediction, 'Accuracy', accuracy)
    
    # Loss
cross_entropy = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y_label_reshape,logits=tf.cast(y2, tf.float32)))

tf.summary.scalar('loss', cross_entropy)
    
# Train
train = tf.train.AdamOptimizer(learning_rate).minimize(cross_entropy, global_step=global_step)
    
    # Saver
saver = tf.train.Saver(max_to_keep=2)


  

#全连接层
#sess=tf.InteractiveSession()  
sess=tf.Session()
sess.run(tf.global_variables_initializer())

for j in range(10000):
  for i in range(500):
 
   #   result=sess.run(train ,feed_dict={x: mf,y_label:yl})
   # mf=[1,1,x[i]]
   # mf=[1,1,[1.2910222314028247e-05, 1.2910222314028247e-05, 2.5820444628056494e-05, 2.5820444628056494e-05, 3.873066694208474e-05]]
    list_a=[]

    #for li in x[i:i+10]:
     #  list_a.append(tf.expand_dims(li,0))

    mf=tf.expand_dims(x[i],0)

    mf=tf.expand_dims(mf,0)
  #  mf=tf.stack(list_a, axis=0)  
   # print(mf)
   
    x_feed=sess.run(mf)

    y_feed=sess.run(tf.expand_dims(y_t[i],0))
   # print(y_feed)
    _,acc,loss,predict=sess.run([train,accuracy,cross_entropy,y_predict] ,feed_dict={x_input:x_feed,y_label:y_feed})
    print("loss:",loss)
    print("i= ",i)
    if loss<0.1:
       print(y_predict)
       print(y_feed)

       print("acc:",acc)
       print("loss:",loss)


