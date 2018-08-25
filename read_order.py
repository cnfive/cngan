import sys
import re


filepath="/media/hadoop/文档/simplechat-master/order.txt"
file=open(filepath)
order={}


for line in file:
    if len(line.strip())>10:
       print(line)
       seq=line.split("	")
       orderid=seq[0].strip()
       user_id=seq[1].strip()
       product=seq[3].strip()
       attribute=seq[4].strip()

       print(seq[4])
       if attribute=="1":
          print("我要修改电话")
          print("我要修改地址")
          print("我要撤单")
       if attribute=="2":
          print("赶快发货，我等不急了")
       if attribute=="3":
          print("我取消订单，啥时候钱到卡上")
       if attribute=="4":
          print("我遇到安装问题")
          print("我要返修")
          print("品质不一样，我要退货")
          print("")
       else:
          print(attribute)
       order[orderid]=[user_id,product,attribute]

file.close()

filepath="/media/hadoop/文档/simplechat-master/chat9.txt"
file = open(filepath)
print("***********现在开始对话*************")
s_list=[]
i=0
sentence=[]
para=[]
paragrapha={}
all_sentence=[]
tag="00029c51f92e8f34250d6af329c9a8df"
for line in file:
     #line_split=line[56:]

     i=i+1
     #if i>12821:
     #   break
     line_split=line.split("	")
     #print(line_split[6])
     s=line_split[6]
     session_id=line_split[0]
     user_tag=line_split[2]

     #user_tag=int(user_tag)+1

     if tag == line_split[0]:
        para.append(user_tag)
        para.append(s.strip())
        all_sentence.append(s.strip())
     else:
        paragrapha[session_id]=para
        para=[]

        para.append(user_tag)
        para.append(s.strip())
        all_sentence.append(s.strip())

     tag=session_id

     if i>12808:
        break
     if s not in sentence:
        sentence.append(s.strip())
#print(paragrapha)
for key in  paragrapha:
     #print(key)
     chat_group=paragrapha[key]
     tag=0
     order_id=0
     for sentence in chat_group:
         m = re.search("ORDERID_\d+",sentence)
         if m!=None:

             print(m.group())
             order_id=m.group()
         
             tag=1
             
             if order_id in order: 
                  txt=order[order_id]
                  print(txt)
     if tag==1:
         print(chat_group) 
     
     












