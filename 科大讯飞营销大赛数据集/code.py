import pymysql
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import matplotlib.pyplot as plt
import random
import time
import re

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
