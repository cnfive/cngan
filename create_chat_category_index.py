# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import sys,os
#sys.path.append("../")
from whoosh.index import create_in,open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser

from jieba.analyse import ChineseAnalyzer

analyzer = ChineseAnalyzer()

schema = Schema(title=TEXT(stored=True),  content1=TEXT(stored=True, analyzer=analyzer),content2=TEXT(stored=True, analyzer=analyzer))
if not os.path.exists("tmp"):
    os.mkdir("tmp")

ix = create_in("tmp", schema,indexname="chat_index") # for create new index
#ix = open_dir("tmp") # for read only
writer = ix.writer()

filepath="./项目代码/sentence_count_user_type_0.txt"
file1 = open(filepath)
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
            sentence=seq[3].strip()
            u_line_tag=seq[2].strip()
            para.append([sessionid,line_num,sentence,u_line_tag])

            paragrapha[tag,u_tag]=para

      #if sent_num>50000:
          #  break

      #sent_num+=1
  
file1.close()
filepath="./项目代码/sentence_count_user_type_1.txt"

file2 = open(filepath)
for line in file2:
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
            sentence=seq[3].strip()
            u_line_tag=seq[2].strip()
            para.append([sessionid,line_num,sentence,u_line_tag])

            paragrapha[tag,u_tag]=para

file2.close()

for key in  paragrapha:

   txt=paragrapha[key]
 
   line=""

   if  key[1]=="0":
        #for txt in paragrapha[key]:
        #      line=line+" "+txt[2]
        line=(paragrapha[key][0])[2]
        writer.add_document(title=key[0],content1=line  )
   if  key[1]=="1":

        #for txt in paragrapha[key]:
              #line=line+" "+txt[2]
        line=(paragrapha[key][0])[2]      
        writer.add_document(title=key[0],content2=line  )

writer.commit()
print("索引生成结束！")
