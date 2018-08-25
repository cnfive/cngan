import os

import re

filepath="/media/hadoop/文档/simplechat-master/chat_copy.txt"
file1 = open(filepath)
print("***********现在开始对话*************")
s_list=[]
i=0
sentence2=[]
para=[]
paragrapha={}
all_sentence=[]


tag=""
  #first_tag=""
sentence_order=[]
for line in file1:

   #i=i+1

   i=i+1
  # if i>pcount:
     #   break
   if len(line)>1 :
   
     
     #if i>12821:
     #   break
     line_split=line.split("	")
     #print(line_split[6])
     s=line_split[6]
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
     if i==212807:
          paragrapha[tag]=para
          para=[]
          break

file1.close()




count=0

f = open("chat_new2.txt", 'w')
for session in paragrapha:

       count=count+1
       dic={}
       print("page count:"+str(count))
       id_list=[]
       s_and=""
       list_u_tag=[]
       first_tag=""
       u_id=""
       u_tag=""
       first_session=""
       for key in paragrapha[session]:
             print(key)
             s=key[2]
    #print(s)
             u_id=key[0]
             u_tag=key[1]
      #       first_session
             if first_tag!="":

                if   first_tag==u_tag:

  
                     s_and+="，"+s
                else:

                     if u_tag=="0":
                        tag="1"

                     else:

                        tag="0"
                        
                     f.writelines(session+"	"+u_id+"	"+tag+"	"+s_and+"\n")
                     s_and=s


             else: 
                     s_and=s

             first_session=session

             first_tag=u_tag


             #if session!=first_session:
       if u_tag=="0":

            tag="0"

       else:

            tag="1"

       f.writelines(session+"	"+u_id+"	"+tag+"	"+s_and+"\n")                          

f.close()




