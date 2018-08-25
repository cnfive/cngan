import tensorflow as tf


filepath="./feature_200w.txt"

f=open(filepath,"r")

i=0
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
                dic[word]=i

                i=i+1
            if word!='':
               word_seq2.append(word)
   # print(word_seq2)
    chat_list.append(word_seq2)

f.close()
#senten to id

chat_sentence_id_list=[]
#print(dic)

for session in chat_list:
    sentence_to_id=[]
    for sentence in session :
         sentence_to_id.append(dic[sentence])
    chat_sentence_id_list.append(sentence_to_id)

#print(chat_sentence_id_list)
print(len(dic))





