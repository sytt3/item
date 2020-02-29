import requests
import re
import time
import random
import xlwt
import xlrd
from xlutils.copy import copy
header={
    'cookie':'cna=5TH+FM7ohksCAXFFnnp5x5Fq; x=__ll%3D-1%26_ato%3D0; OZ_1U_2061=vid=vd7e64eeb91c9a.0&ctime=1568564586&ltime=1568564585; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie14=UoTUO8RH66baSg%3D%3D; uc3=vt3=F8dBxdsbCJ7A8UyT4gg%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&id2=UUpmlcrVKWLsRg%3D%3D&nk2=r7kxc6F1%2BMQ%3D; t=ff14e8195b762e9ce6702240a85174c6; tracknick=%5Cu5929%5Cu5B57%5Cu5C71%5Cu53F7; lid=%E5%A4%A9%E5%AD%97%E5%B1%B1%E5%8F%B7; uc4=nk4=0%40rVtLF%2BMi8KRzcfcLSFJ3u1BLhg%3D%3D&id4=0%40U2gsGTC6AenCaZVffow2try%2BDjQT; lgc=%5Cu5929%5Cu5B57%5Cu5C71%5Cu53F7; enc=aOcC0kyv2BCouhmezbviIsJq0f8BFVz66zr8D8oZl%2BQ0Q7CpItvgrxw%2FlHCW1%2BrDOjS0zY397%2BnplR1kXsF3uw%3D%3D; _tb_token_=7ee75eb3193eb; cookie2=1e95e860ebfe1fda55a9e541d8833bf0; x5sec=7b22726174656d616e616765723b32223a22633530316131313537626634336636346634656563663065366266313130653143502f756976494645493671792f79573574327948773d3d227d; l=cBxBoqIuvwVCsjIUBOfwRuI8LO7O3IR34kPzw4OGbICP_y59a9mPWZV2S9TpCnGVp6HXR3JjcDOTBeYBqCqgx6aNa6Fy_; isg=BOLiX5JYyH9xt9YWrlq2XJ1lPWhEM-ZNNMfQ1ix7kNT3_4J5FMHAXDtxLzsDdF7l',
    'referer':'https://detail.tmall.com/item.htm?id=569134471494&ali_refid=a3_430583_1006:1125104673:N:i6zRTdnDrO/M84mQPSQ5hQ==:7ae5705133db0ca338e71213e7ebdd6f&ali_trackid=1_7ae5705133db0ca338e71213e7ebdd6f&spm=a230r.1.14.1',
    'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'
    }

url='https://rate.tmall.com/list_detail_rate.htm'
text=[]

def append_xls(text):
    rb=xlrd.open_workbook('text.xls')
    rb1=rb.sheet_by_name(rb.sheet_names()[0])
    wb=copy(rb)
    wb1=wb.get_sheet(0)
    wb1.write(rb1.nrows+1,0,text)
    wb.save('text.xls')
def get_data():    
    for i in range(100,200):
        params={
            'itemId':'569134471494',
            'sellerId':'3081047815',
            "currentPage":str(i+1)
            }
        req=requests.get(url,params,headers=header).text
        p=re.compile(r'rateContent\S+fromMall')
        content=p.findall(req)
        text=text+content
        print('第%d页内容节选'%i,content[0])
        time.sleep(5*random.random()+0.1)
    
content=''
rb=xlrd.open_workbook('text.xls')
rb1=rb.sheet_by_name(rb.sheet_names()[0])
for i in range (rb1.nrows):
    content+=rb1.cell_value(i,0)

list_content=content.split('rateContent":"')
for x in list_content:
    if x !='


























    
