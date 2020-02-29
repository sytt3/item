import re
import time
import random
import xlwt
import xlrd
from xlutils.copy import copy
import pandas as pd
import datetime
import matplotlib.pyplot as plt
def get_database():
    import requests
    from bs4 import BeautifulSoup
    #url='http://fund.eastmoney.com/007300.html'
    header={
        #'referer':'http://fund.eastmoney.com/110011.html',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'
        }
    '''
req=requests.get(url,headers=header)
req.encoding='utf-8'
req=req.text
soup=BeautifulSoup(req,'lxml')
name=soup.findAll(name='td',attrs={'class':'alignLeft'})
rate=soup.findAll(name='td',attrs={'class':'alignRight bold'})
#profit_month=soup.findAll(name='span',attrs={'class':'ui-font-middle ui-color-green ui-num'})[0].string
#profit_season=soup.findAll(name='span',attrs={'class':'ui-font-middle ui-color-green ui-num'})[1].string

profit_month_tag=soup.findAll('dd')[1]
profit_season_tag=soup.findAll('dd')[4]
profit_month=profit_month_tag.contents[1].string
profit_season=profit_season_tag.contents[1].string
syt={}
for i in range(10):
    syt[next(name[i].a.children)]=rate[i*2].string
    '''


    url='http://fund.eastmoney.com/data/rankhandler.aspx'
    data={}
    ed=datetime.date.today()
    sd=ed-datetime.timedelta(days=365)
    params={
      'op':'ph',
      'dt':'kf',
      'ft':'gp',
      #'rs'='gs',
      'gs':'0',
      'sc':'3nzf',
      'st':'desc',
      'sd':sd.strftime('%F'),
      'ed':ed.strftime('%F'),
      'qdii':'',
      'pi':1,
      'pn':'550',#设置爬取基金数
      'dx':'1'}
    req=requests.get(url,params,headers=header)
    req.encoding='utf-8'
    req=req.text
    s=req.split(u'",')
    for jj in s:
        y=jj.split(',')
        num=y[0][-6:]
        name=y[1]
        month=y[8]
        season=y[9]
        year_1=y[11]
        year_2=y[12]
        year_3=y[13]
        data[name]=[num,month,season,year_1,year_2,year_3]

    data1=pd.DataFrame.from_dict(data,orient='index')
    columns_name=['num','month','season','year_1','year_2','year_3']
    data1.columns=columns_name

    #data1.to_excel('GuPiao.xls')

    data2={}
    for num in data1.num:
        try:
        
            url='http://fund.eastmoney.com/%s.html'%str(num)
            req=requests.get(url,headers=header)
            req.encoding='utf-8'
            req=req.text
            soup=BeautifulSoup(req,'lxml')
            name=soup.findAll(name='td',attrs={'class':'alignLeft'})
            #rate=soup.findAll(name='td',attrs={'class':'alignRight bold'})
            jj_name=soup.findAll(name='div',attrs={'style':'float: left'})[0].contents[0]
            rank=[]
            for i in range(10):
                rank.append(next(name[i].a.children))
            data2[jj_name]=rank
            time.sleep(random.random())
            print('已爬到%s'%jj_name)
        except AttributeError:
            print('该基金无股票持仓—%s'%str(num))
        continue

    #碰到前10无持仓的，需要打断错误继续执行

    col_name=['rank_'+str(i) for i in range(1,11)]
    data3=pd.DataFrame.from_dict(data2,orient='index')
    data3.columns=col_name
    data4=pd.concat([data1,data3],axis=1)
    data4.to_excel('GuPiao.xls')
    return data4

def get_rank(data,top):
    syt=pd.Series([])
    rank_list=['rank_'+str(i) for i in range(1,top+1)]
    for x in rank_list:
        syt=syt.append(data[x])
    rank=syt.value_counts()
    return rank


def select_data(data,month=0,season=0,year_1=0,year_2=0,year_3=0):
    a=data[data.month>month]
    b=a[a.season>season]
    c=b[b.year_1>year_1]
    d=c[c.year_2>year_2]
    data1=d[d.year_3>year_3]
    return data1
def wordcloud(rank):
    #Ps:词云图，敲代码还没有抠图时间长，美图扣的出来的，背景需要改成透明的，否则读取时还是一张完整的矩形图
    import wordcloud
    import numpy as np
    from PIL import Image
    mask=np.array(Image.open('money.jpg'))#,此处可添加背景图
    wc=wordcloud.WordCloud(
        font_path='C:/Windows/Fonts/simhei.ttf', # 设置字体格式
        mask=mask, # 设置背景图形状
        background_color='white',
        max_words=200, # 最多显示词数
        max_font_size=100 # 字体最大值
        )
    wc.generate_from_frequencies(rank)
    image_colors = wordcloud.ImageColorGenerator(mask)
    wc.recolor(color_func=image_colors)
    plt.imshow(wc)
    plt.axis('off')
    plt.show()
    
if __name__=='__main__':
    data=pd.read_excel('Gupiao.xls')
    rank=get_rank(data,10)












    
