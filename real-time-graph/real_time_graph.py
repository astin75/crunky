# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:06:01 2019

@author: A
"""

#project  Sand castle

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file,save
from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT
from bokeh.io import export_png
from IPython.display import HTML
import pandas as pd
import os, sys, re, time
from datetime import datetime
from random import *
import numpy as np
import matplotlib as mpl
%matplotlib inline
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import seaborn as sns
from plotnine import *
import platform
from pandas import DataFrame as df


from matplotlib import font_manager, rc
plt.rcParams['axes.unicode_minus'] = False

if platform.system() == 'Darwin':
   rc('font', family='AppleGothic')
elif platform.system() == 'Windows'    :
   path = "c:/Windows/Fonts/malgun.ttf"
   font_name = font_manager.FontProperties(fname=path).get_name()
   rc('font', family=font_name)
else:
   print('Unknown system')

# html template out by jin ja ----------------------------------------

import jinja2
chatsize = os.stat('chattest1.csv')
size=chatsize.st_size
size= str(size / 1024)
size = size[0:6]

template_size = jinja2.Template('''\
<html>
<head>
<style>
#sbox{width:200px;
text-align:center;
margin-left:20px;}


#one {width:150px;
border: 2px solid #bcbcbc;
}


</style>
</head>

<body style="background-color:#e6e4e3;">
<div id="sbox">
<h1>File size</h1>
<hr id="one"><h2>
{{size}} KB

</h2>
</div>

</body>

</html>
''')
now = datetime.now()
template_time = jinja2.Template('''\
<html>
<head>
<style>
#sbox{width:200px;
text-align:center;
margin-left:20px;}


#one {width:150px;
border: 2px solid #bcbcbc;
}


</style>
</head>

<body style="background-color:#e6e4e3;">
<div id="sbox">
<h1>Time</h1>
<hr id="one"><h2>
{{now.hour}} :
{{now.minute}} :
{{now.second}}
</h2>
</div>

</body>

</html>
''')
template_row = jinja2.Template('''\
<html>
<head>
<style>
#sbox{width:200px;
text-align:center;
margin-left:20px;}


#one {width:150px;
border: 2px solid #bcbcbc;
}


</style>
</head>

<body style="background-color:#e6e4e3;">
<div id="sbox">
<h1>Table row</h1>
<hr id="one"><h2>
{{row}}

</h2>
</div>

</body>

</html>
''')


# html template out by jin ja  -----------------------------------------------

# 실시간 채팅 그리기 
def g1(vol):
    # 변수를 담을 상자 및 데이터 프레임 
    box=[]
    box2= []
    x1= []
    y1= []
    final = pd.DataFrame({'미국':[1],
                      '일본':[2],
                      '영국':[3],
                      '프랑스':[4], 
                      '독일':[5],
                      '대한민국':[6],
                      '중국':[7]}) 


    af1 = pd.read_csv('../data/rent/seoul_db_1.csv', encoding='euc-kr')        #서울맵 그래프를 그리기위한 csv 파일 

    p = figure(plot_width=780, plot_height=332, background_fill_color="#566573")  # bokeh 그래프 figure
    p2 = figure(plot_width=780, plot_height=140, background_fill_color="#E5E7E9") # bokeh 그래프 figure
    p3 = figure(plot_width=335, plot_height=332, background_fill_color="#566573") # bokeh 그래프 figure

    for test1 in range(1,vol):
        c = randint(1, 1381072)  #서울맵 그래프를 random 하게 그리기 위한 설정  
        c1 = randint(1, 1381072)
        c2 = randint(1, 1381072)
        try:
              
            af = pd.read_csv('chattest1.csv')   # 실시간 채팅 csv 파일을 불러온다. 

            chatsize = os.stat('chattest1.csv')

            # 파일 사이즈, 행 그리고 시간을 표기 하기위한 설정 
            row= len(af)
            now = datetime.now()
            chatsize = os.stat('chattest1.csv')
            size=chatsize.st_size
            size= str(size / 1024)
            size = size[0:6]
            
            
            df = af
            df['bin'] = 1 # 1의 값을 가지는 빈도수 행을 생성 
            df2  = df.groupby(df['text'])[["bin"]].sum()  # 같은 채팅 내용을 더한다. 
            df2['count'] = 1  
            df2  = df2.groupby(df2['bin'])[["count"]].sum()   # 빈도수를 기준으로 랭킹화 
            df2 = df2.sort_values(by = 'count',ascending=False)
            df2 = df2.reset_index()
            

            if len(df2['count']) >=7: # 랭킹 수가 7개 이상일때만 진행
                for i in range(0,7):

                    b = 'box%d' %i
                    box.append(b)
                    box[i] = []
                    a = df2['count'][i]
                    box[i].append(a)       # 각 랭킹을 box에 담는다  (1,2,3...7)           
                
                    
                fapp = pd.DataFrame({'미국':box[0],        #df 생성
                                      '일본':box[1],
                                      '영국':box[2],
                                      '프랑스':box[3], 
                                      '독일':box[4],
                                      '대한민국':box[5],
                                      '중국':box[6]})
                

                # 그래프 생성 -------------------------
                box2.append(test1)
                varc = len(box2)
                fapp['count1'] = varc # for var chat
                
                time.sleep(1)
                final = pd.concat([final,fapp])
                final = final.reset_index()
                del final['index']



                #ssum = final['미국']+final['일본']+final['중국']+final['독일']+final['대한민국']+final['프랑스']+final['영국']
                p.line(final.index, final['미국'],line_color="#F1C40F",legend='US')
                p.line(final.index, final['일본'],line_color="#EC7063" ,legend='JP')
                p.line(final.index, final['영국'],line_color="#5DADE2",legend='UK')
                p.line(final.index, final['프랑스'],line_color="#48C9B0",legend='FR')
                p.line(final.index, final['독일'],line_color="#DC7633",legend='DE')
                p.line(final.index, final['대한민국'],line_color="#117864",legend='KR')
                p.line(final.index, final['중국'],line_color="#AF7AC5",legend='CN')
                #p.line(final.index, ssum,line_color="#5D6D7E")
                p.legend.location = 'top_left'
                export_png(p, filename="g1.png")
                save(p)
                
                #var stack
                county = ["미국", "일본", "영국", "프랑스", "독일", "대한민국", "중국"]
                colors = ["#F1C40F", "#EC7063", "#5DADE2", "#48C9B0", "#DC7633", "#117864", "#AF7AC5"]
                p3.vbar_stack(county,x='count1',  width=0.8, color=colors, source=final)
                export_png(p3, filename="b1.png")
                save(p3)
                
                #total line
                ssum = final['미국']+final['일본']+final['중국']+final['독일']+final['대한민국']+final['프랑스']+final['영국']
                p2.line(final.index, ssum,line_color="#2E86C1",legend='Total')
                p2.legend.location = 'top_left'
                export_png(p2, filename="g2.png")
                save(p2)
                
                #scatter
                x3=af1['경도'][c2]
                x2=af1['경도'][c1]
                x=af1['경도'][c]
                y3=af1['위도'][c2]
                y2=af1['위도'][c1]
                y=af1['위도'][c]
                x1.append(x)
                x1.append(x2)
                x1.append(x3)
                y1.append(y)
                y1.append(y2)
                y1.append(y3)
                colors = cm.rainbow(np.linspace(0, 1, len(y1)))
                fig = plt.figure(figsize=(4.6,4.3))
                plt.scatter(x1,y1, c=colors, alpha=0.4)
                plt.savefig('seoulsc.png')
                
                
                
                #data view

                HTML(template_size.render(size=size))
                with open('filesize.html','w') as f:
                    f.write(template_size.render(size=size))
                    
                
                HTML(template_time.render(now=now))
                with open('time.html','w') as f:
                    f.write(template_time.render(now=now))
                    
                HTML(template_row.render(row=row))
                with open('tablerow.html','w') as f:
                    f.write(template_row.render(row=row))
                #data view out
                
                if len(af) >= 49500:
                    break
        except:
            print(test1)

