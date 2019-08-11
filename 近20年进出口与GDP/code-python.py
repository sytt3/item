import pymysql
import pandas as pd
from pandas import DataFrame,Series
import numpy as np
import matplotlib.pyplot as plt


'''
#从数据库中导入数据
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


'''
第二种取数方法
直接用SQL语句预处理数据，减少取数
'''
'''
#从数据库中取数
db=pymysql.connect(host='localhost',user='root',password='password',database='items1',charset='utf8')
cur=db.cursor()
SQL='SELECT data.*,gdp.gdp  FROM data LEFT JOIN gdp ON data.year=gdp.year'#MySQL记得一定需要把gdp中的year给删除了，否则后面list转化时，会自动屏蔽一项year造成表头位数与columns不匹配
cur.execute(SQL)
data=cur.fetchall()
_=cur.description
cur.close()
columns1=[]
for x in _:
    columns1.append(x[0])
data=DataFrame(list(data),columns=columns1)
data=data.set_index(data['year'])
data=data.drop('year',axis=1)
'''

'''
数据整合：整合单位存在万吨，也存在吨；将object转换成float，否则后续无法进行运算；处理缺失值
'''
#处理缺失值，注：pandas将NONE当做缺失值，所以直接用fillna就行
data=data.fillna(0)
data=data.astype(float)
data[[u'铜材出口量(吨)',u'铝材出口量(吨)',u'锌及锌合金出口量(吨)']]/=10000


'''
绘图1，描述进出口量历年变化
'''
def analyse1(data):
    a=list(data)#读取data表头
    M=[_ for _ in a if u'进口' in _]#区分进口、出口
    X=[_ for _ in a if u'出口' in _]

    fig=plt.figure(figsize=(25,6)) #建立图幅，figsize设计图幅大小
    plt.rcParams['font.sans-serif']=['SimHei'] #解决matplotlib中文乱码问题
    axM=fig.add_subplot(121)  #建立子图，图幅为1行2列，占在第一个图框中
    plt.title('Import')
    plt.plot(data.index,data[M])#折线图
    plt.xlabel('year')
    plt.ylabel('quantity')
    plt.legend(list(data[M]),loc='best')#将图例添加入图幅中

    axX=fig.add_subplot(122)
    plt.title('Export')
    plt.plot(data.index,data[X])
    plt.xlabel('year')
    plt.ylabel('quantity')
    plt.legend(list(data[X]),loc='best')
    plt.show()

'''
绘图2，找出各类物品进/出口最大量的一年
'''
def analyse2(data):
    fig=plt.figure(figsize=(30,8))
    plt.rcParams['font.sans-serif']=['SimHei']
#plt.yticks(np.linspace(0,8,18),np.arange(2000,2018))
    plt.scatter(list(data),data.idxmax(axis=0))
    #plt.scatter(list(data),data.idxmin(axis=0))
    plt.xlabel(u'主要高耗能产品')
    plt.ylabel(u'Year')
    plt.title(u'进出口产品峰值年')
    plt.xticks(rotation=-15)
    #plt.legend(['max','min'],'best')
    plt.show()








































