import pymysql
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import re

plt.rcParams['font.sans-serif']=['SimHei']
db=pymysql.connect(host='localhost',user='root',password='password',database='item2',charset='utf8')
sql='''
SELECT *
FROM train_set
'''
data=pd.read_sql(sql,db)
def Hour(data):
    data.time=data.time.astype('int64')
    def get_hour(timestamp):
        s=time.localtime(timestamp)
        return s.tm_hour
    return data.time.apply(func=get_hour)
def count_unique(data):
    counts=[]
    for _ in list(data):
        counts.append(len(data[_].unique()))
    return DataFrame(counts,index=list(data),columns=[u'字段'])

def tur_model(data):
    data.model=data.model.str.lower()
    s=data.model.fillna('syt')
    lst=[]
    for x in s:
        lst.append(''.join(re.findall(u'[a-z0-9]',x)))
    return lst

def explore(data):
    fig=plt.figure(figsize=(25,6))
    values=[data.click.sum(),data.click.count()-data.click.sum()]
    ax1=fig.add_subplot(221)
    plt.pie(values,labels=['点击','未点击'],shadow=True,autopct='%1.1f%%')
    plt.title('点击率')

    ax2=fig.add_subplot(222)
    grouped1=data['click'].groupby(data['time'])
    time_click_rate=grouped1.sum()/grouped1.count()
    plt.bar(time_click_rate.index,time_click_rate.values)
    plt.title('各时间段点击率')

    '''
    ax3=fig.add_subplot(223)
    a=data[['make','click']]
    a=a.dropna(axis=0)
    grouped2=a.click.groupby(a['make'])
    make_click_rate=grouped2.sum()/grouped2.count()
    plt.barh(make_click_rate.index,make_click_rate.values)
    plt.title('手机品牌作用性')
'''
    ax3=fig.add_axes([0.05,0.05,0.55,0.4])
    grouped3=data['click'].groupby(data['advert_industry_inner'])
    inner_click_rate=grouped3.sum()/grouped3.count()
    ax3.bar(inner_click_rate.index,inner_click_rate.values)
    plt.title('广告主行业作用性')
#由于手机品牌太多，还是直接看数吧，画图画不出来

    ax4=fig.add_subplot(224)
    grouped4=data['click'].groupby(data['province'])
    area_click_rate=grouped4.sum()/grouped4.count()
    plt.bar(area_click_rate.index,area_click_rate.values)
    plt.title('地域作用性')

    

    plt.show()
    
    plt.pie

def explore1(data,feature):
    G=data.click.groupby(data[feature])
    rate=G.sum()/G.count()
    graph=plt.bar(rate.index,rate.values)
    plt.title(feature)
    return graph,rate

def Get_P(data,feature):
    '''
data ----输入的数据
feature ----表示想要查询的字段特征

输出
fre ----feature下各情况的频率 即P(w)
rate ----feature下各情况的点击概率 即P(W|c)
    '''
    a=data[feature].unique()
    fre={}
    for _ in a:
        rate1=list(data[feature]).count(_)/data[feature].count()
        fre[_]=rate1
    G=data.click.groupby(data[feature])
    rate2=G.sum()/G.count()
    return fre,rate2
