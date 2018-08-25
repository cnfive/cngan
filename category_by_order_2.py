
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
     #pattern = re.compile("ORDERID_\d+")
    # out = re.sub(pattern, '订单号', s_strip)
     #pattern2 = re.compile("\d+")
    # out = re.sub(pattern2, '[数字x]', s_strip)
     out=s_strip
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

product_category=[]

filepath="/media/hadoop/文档/simplechat-master/order.txt"
file2=open(filepath)
order={}


for line in file2:
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

       if product not in product_category:
              product_category.append(product)

file2.close()
print(product_category)
#input()

sentence_catgegory={}
#product_category=[]

for key in  paragrapha:
     #print(key)
     chat_group=paragrapha[key]
     tag=0
     order_id=0
    # print(chat_group)
     txt=""
     for sentence in chat_group:
     
         m = re.search("ORDERID_\d+",sentence[2])
         if m!=None:

             print(m.group())
             order_id=m.group()
         
             tag=1
             
             if order_id in order: 
                  txt=order[order_id]
                  print(txt)
                  
     if tag==1:
         print(chat_group) 
         print(txt)
         if txt!="":
            if txt[2]=="4":
               print("分类A")
                #按产品类目分类
               if ("a",txt[1]) not in sentence_catgegory:
                  sentence_catgegory[("a",txt[1])]=[key]
              
               else:
  
                  list_a=sentence_catgegory[("a",txt[1])]

                  if key not in list_a:
                     list_a.append(key)
                     sentence_catgegory[("a",txt[1])]=list_a

            if txt[2]=="3":
               print("分类B")

               if ("b",txt[1]) not in sentence_catgegory:
                  sentence_catgegory[("b",txt[1])]=[key]
              
               else:
  
                  list_a=sentence_catgegory[("b",txt[1])]

                  if key not in list_a:
                     list_a.append(key)
                     sentence_catgegory[("b",txt[1])]=list_a

            if txt[2]=="2":
               print("分类c")

               if ("c",txt[1]) not in sentence_catgegory:
                  sentence_catgegory[("c",txt[1])]=[key]
              
               else:
  
                  list_a=sentence_catgegory[("c",txt[1])]

                  if key not in list_a:
                     list_a.append(key)
                     sentence_catgegory[("c",txt[1])]=list_a

            if txt[2]=="1":
               print("分类D")

               if ("d",txt[1]) not in sentence_catgegory:
                  sentence_catgegory[("d",txt[1])]=[key]
              
               else:
  
                  list_a=sentence_catgegory[("d",txt[1])]

                  if key not in list_a:
                     list_a.append(key)
                     sentence_catgegory[("d",txt[1])]=list_a
         else:
               print("分类E")

               if ("e","0") not in sentence_catgegory:
                  sentence_catgegory[("e","0")]=[key]
              
               else:
  
                  list_a=sentence_catgegory[("e","0")]

                  if key not in list_a:
                     list_a.append(key)
                     sentence_catgegory[("e","0")]=list_a


     else:
               print("分类F")

               if ("f","7") not in sentence_catgegory:
                  sentence_catgegory[("f","7")]=[key]
              
               else:
  
                  list_a=sentence_catgegory[("f","7")]

                  if key not in list_a:
                     list_a.append(key)
                     sentence_catgegory[("f","7")]=list_a
    ###############这些分类下面再按产品分类，再下一级按q,a 分类
          
#print(sentence_catgegory)   

filename="./sentence_count_user_type_0.txt"

print("读取语料")
  
file1 = open(filename)
  
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
u_tag=""
for line in file1:
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
  
file1.close()

session_id_category={}
gobal_line=[]

for  category in sentence_catgegory:
       print(category)
    #   print(sentence_catgegory[category])

       for session_id in sentence_catgegory[category]:

             print(session_id)

             for key in paragrapha:
                   # print(key)

                    list_line=paragrapha[key]

                    for line in list_line:

                          if  session_id==line[0] and [key[0],key[1]]  not in gobal_line:

                             if category not in session_id_category:
                                #if line not in session_id_category[category]:
                                    list_c=[]
                                    list_c.append([key[0],key[1]])

                                    session_id_category[category]=list_c

                                    gobal_line.append([key[0],key[1]])
                             else:
                                    if [key[0],key[1]] not in session_id_category[category]:
                                            
                                           list_c= session_id_category[category]

                                           list_c.append([key[0],key[1]])

                                           session_id_category[category]=list_c
                                           gobal_line.append([key[0],key[1]])


             #if session_id in 


f_tag=0
r_count=0
r_count2=0
u_tag=0
f=open("./category_by_order.txt","w")
for category in session_id_category:
     print(category)

    # print(session_id_category[category])
     print("........................")
     f.writelines("result_u_"+str(f_tag)+"_"+str(r_count)+"  "+str(u_tag)+"  "+"*************************************************"+"\n")
     for line in  session_id_category[category]:
           print(line)
           c_line=paragrapha[(line[0],line[1])][0]
           print(c_line)
           f.writelines(c_line[0]+"        "+str(c_line[1])+"        "+str(u_tag)+"        "+c_line[2].strip()+"\n")

     r_count=r_count+0
f.close()
print("end")

