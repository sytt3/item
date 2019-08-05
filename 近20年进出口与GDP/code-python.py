import pymysql
import pandas as pd
from pandas import DataFrame,Series
import numpy as np

'''
从数据库中导入数据
'''
db=pymysql.connect(host='localhost',user='root',password='password',database='items1',charset='utf8') #连接数据库
cur=db.cursor() #建立游标
SQL1='SELECT * FROM gdp'  #建立需要使用的SQL语句，共两条  
SQL2='SELECT * FROM data'

#执行语句，注意，execute语句会形成一个缓存空间，记得及时将数据提取出来，否则会被刷新掉
cur.execute(SQL1)
gdp=cur.fetchall()
cur.execute(SQL2)
data=cur.fetchall()

#获取表头数据，省去一大堆中文
_=cur.description
columns1=[]
for x in _:
    columns1.append(x[0])
cur.close()#关闭连接

#将二维元组转换为DataFame结构，需注意的是二维元组（（1,2），（2,3））无法组成DataFrame结构，需要先转换成List
data=DataFrame(list(data),columns=columns1)
data=data.set_index(data['year'])
data=data.drop('year',axis=1)
gdp=DataFrame(list(gdp))
gdp=gdp.set_index(gdp[0])
gdp=gdp.drop(0,axis=1)
gdp.rename(columns={1:'生产总值'},inplace=True)
#gdp=gdp.rename({1:'生产总值'},inplace=True) 此处注意，修改列名时必须指出columns

data['生产总值']=gdp #合并表格，将gdp表中的生产总值增添到data中，注：由于将index改为了年份，增添数据时，会自动对齐index
