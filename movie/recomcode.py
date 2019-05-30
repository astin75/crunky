# -*- coding: utf-8 -*-
"""
Created on Sun May 12 09:27:02 2019

@author: Administrator1
"""

import pandas as pd
import re
import numpy as np
from difflib import SequenceMatcher, get_close_matches


print('DB 로드중 .. ')
df = pd.read_csv('movie313003.csv', encoding='euc-kr')

mc = len(df.title.unique())
user = len(df.userid.unique())
riv = len(df)
print('영화 : {0}'.format(mc))
print('유저 : {0}'.format(user))
print('리뷰 : {0}'.format(riv))




def recommend(mv):
        dfa = pd.DataFrame({ # DF 만들기
                    'userid':[1],
                   'title':[1],
                   'point':[1],
                   'pn':[1],
                   'dirc1':[1],
                   'dirc2':[1],
                   'act1':[1],
                   'act2':[1],
                   'act3':[1],
                   'gen1':[1],
                   'gen2':[1],
                   'gen3':[1]})
        
        a = df.loc[df['title']==mv] # 유저가 입력한 영화를 db에서 찾는다.
        
        #영화 타이블 구하기 1
        dfa1 = dfa
        for i in a['userid'].unique(): 
            #b = df.loc[df['point']>=1]
            #b = b.loc[b['userid']==i]
            b = df.loc[df['userid']==i]
            dfa1 = pd.concat([dfa1, b]) #검색 한 영화를 본사람들을 불러온다.
            
            
        #영화 타이블 구하기 2
        dfa1 = dfa1.loc[dfa1['title']!=mv]
        dfa1 = dfa1.loc[dfa1['title']!=1]
        dfa1['sum'] = 1
        df2  = dfa1.groupby(dfa1['title'])[["sum"]].sum()
        df2 = df2.sort_values('sum', ascending=False)
        df2 = df2.reset_index()   # 그 영화를 본사람들의 영화 리스트 
        
        #영화 타이블 구하기 3
        title_box = []
        rank_box = []
        
        for i in df2.index:
            ti = df2['title'][i]
            tirk = df2['sum'][i]
            tirk1 = 100*(tirk/df2['sum'][0])
            rank_box.append(tirk1)
            title_box.append(ti)
            
        title_rank = pd.DataFrame({'title':title_box,'title_rank':rank_box})
        # 영화리스트를 백분위 시켜 title_rank 라는 df에 저장시킨다. 
        
        
        #영화 감독 구하기 1
        d1 = a['dirc1'].unique()
        d2 = a['dirc2'].unique()
        dt =[d1[0],d2[0]]
        # 그 영화를 찍은 감독명 가져오기 (최대2개로 설정)
        
        #영화 감독 구하기 2
        for i in d1: 
            b = df.loc[df['dirc1']==i]
            b1 = df.loc[df['dirc2']==i]
            dic1 = pd.concat([b,b1])
            nancheck = str(d2[0])
            
            if nancheck == 'nan':
                print('감독2번째는 없습니다.')
                dic1 = dic1.drop_duplicates(['title'])
                tdic = dic1
            else:  
                for n in d2:
                    b = df.loc[df['dirc1']==n]
                    b1 = df.loc[df['dirc2']==n]
                    dic2 = pd.concat([b,b1])   
                    dic1 = dic1.drop_duplicates(['title'])
                    dic2 = dic2.drop_duplicates(['title'])
                    tdic = pd.concat([dic1,dic2])
        tdic = tdic.drop_duplicates(['title'])
        tdic = tdic.reset_index()
        #db에서 그 영화감독이 찍은 영화 들을 다 불러 온다.
        
        
        #영화 감독 구하기 3
        tdic['sum'] = 1
        title_box = []
        rank_box = []
        
        for i in tdic.index:
            ti = tdic['title'][i]
            tirk = tdic['sum'][i]
            tirk1 = 100*(tirk/tdic['sum'][0])
            rank_box.append(tirk1)
            title_box.append(ti)
            
        dic_rank = pd.DataFrame({'title':title_box,'dic_rank':rank_box})
        # 영화리스트를 백분위 시켜 dic_rank 라는 df에 저장시킨다. 
        
        #영화 장르 구하기 1
        g1 = a['gen1'].unique()
        g2 = a['gen2'].unique()
        g3 = a['gen3'].unique()
        gt =[g1[0],g2[0],g3[0]]
        
        #영화 장르 구하기 2
        for i in g1: 
            b = df.loc[df['gen1']==i]
            b1 = df.loc[df['gen2']==i]
            b2 = df.loc[df['gen3']==i]
            gr1 = pd.concat([b,b1,b2])
            nancheck2 = str(g2[0])
            nancheck3 = str(g3[0])
            
            if nancheck2 == 'nan':
                if nancheck3 == 'nan':
                    gr1 = gr1.drop_duplicates(['title'])
                    tgr = gr1
                    print('장르1개')
                    
            elif nancheck2 != 'nan':  
                for n in g2:
                    b = df.loc[df['gen1']==n]
                    b1 = df.loc[df['gen2']==n]
                    b2 = df.loc[df['gen3']==n]
                    gr2 = pd.concat([b,b1,b2])
                    if nancheck3 == 'nan':
                        gr1 = gr1.drop_duplicates(['title'])
                        gr2 = gr2.drop_duplicates(['title'])
                        tgr = pd.concat([gr1,gr2])
                        print('장르2개')
                    else:
                        for m in g3:
                            b = df.loc[df['gen1']==m]
                            b1 = df.loc[df['gen2']==m]
                            b2 = df.loc[df['gen3']==m]
                            gr3 = pd.concat([b,b1,b2])
        
                            gr1 = gr1.drop_duplicates(['title'])
                            gr2 = gr2.drop_duplicates(['title'])
                            gr3 = gr3.drop_duplicates(['title'])
            
                            tgr = pd.concat([gr1,gr2,gr3])
                            print('장르3개')
                            
            tgr = tgr.loc[tgr['title']!=mv]
            tgr = tgr.loc[tgr['title']!=1]
            tgr['sum'] = 1
            tgr  = tgr.groupby(tgr['title'])[["sum"]].sum()
            tgr = tgr.sort_values('sum', ascending=False)
            tgr = tgr.reset_index()
             #db에서 그 영화 장르와 비슷한 영화들을 다 불러 온다.
            
            
            
            #영화 장르 구하기 3
            title_box = []
            rank_box = []
            
            for i in tgr.index:
                ti = tgr['title'][i]
                tirk = tgr['sum'][i]
                tirk1 = 100*(tirk/tgr['sum'][0])
                rank_box.append(tirk1)
                title_box.append(ti)
                
            gen_rank = pd.DataFrame({'title':title_box,'gen_rank':rank_box})
            # 영화리스트를 백분위 시켜 gen_rank 라는 df에 저장시킨다. 
            
            
            
            #영화 배우 구하기 1 (배우는 최대3명 입니다.)
            aa1 = a['act1'].unique()
            aa2 = a['act2'].unique()
            aa3 = a['act3'].unique()
            at =[aa1[0],aa2[0],aa3[0]]
            
            
            for i in aa1: 
                b = df.loc[df['act1']==i]
                b1 = df.loc[df['act2']==i]
                b2 = df.loc[df['act3']==i]
                at1 = pd.concat([b,b1,b2])
                nancheck2 = str(aa2[0])
                nancheck3 = str(aa3[0])
                
            
            #영화 배우 구하기 2 
            if nancheck2 == 'nan':
                if nancheck3 == 'nan':
                    at1 = at1.drop_duplicates(['title'])
                    tat = at1
                    print('배우1명')
                    
            elif nancheck2 != 'nan':  
                for n in aa2:
                    b = df.loc[df['act1']==n]
                    b1 = df.loc[df['act2']==n]
                    b2 = df.loc[df['act3']==n]
                    at2 = pd.concat([b,b1,b2])
                    if nancheck3 == 'nan':
                        at1 = at1.drop_duplicates(['title'])
                        at2 = at2.drop_duplicates(['title'])
                        tat = pd.concat([at1,at2])
                        print('배우2명')
                    else:
                        for m in aa3:
                            b = df.loc[df['act1']==m]
                            b1 = df.loc[df['act2']==m]
                            b2 = df.loc[df['act3']==m]
                            at3 = pd.concat([b,b1,b2])
        
                            at1 = at1.drop_duplicates(['title'])
                            at2 = at2.drop_duplicates(['title'])
                            at3 = at3.drop_duplicates(['title'])
            
                            tat = pd.concat([at1,at2,at3])
                            print('배우3명')
                            
            tat = tat.loc[tat['title']!=mv]
            tat = tat.loc[tat['title']!=1]
            tat['sum'] = 1
            tat  = tat.groupby(tat['title'])[["sum"]].sum()
            tat = tat.sort_values('sum', ascending=False)
            tat = tat.reset_index()
            
            #db에서 그 배우들이 출연한 영화들을 다 불러 온다.
            
            #영화 배우 구하기 3 
            title_box = []
            rank_box = []
            
            for i in tat.index:
                ti = tat['title'][i]
                tirk = tat['sum'][i]
                tirk1 = 100*(tirk/tat['sum'][0])
                rank_box.append(tirk1)
                title_box.append(ti)
                
            act_rank = pd.DataFrame({'title':title_box,'act_rank':rank_box})
            # 영화리스트를 백분위 시켜 act_rank 라는 df에 저장시킨다. 
            
            
            #최종작업 1
            # 앞서 구한 DF를 영화를 기준으로  합칩니다 
            last = pd.merge(title_rank, gen_rank, how='outer')
            last = pd.merge(last, act_rank, how='outer')
            last = pd.merge(last, dic_rank, how='outer')
            
            
            
            #최종작업 2 각행들을 불러오고
            last_title = []
            score_box = []
            for i in last.index:
                title = last['title'][i]
                a = last['title_rank'][i]
                b= last['gen_rank'][i]
                c = last['act_rank'][i]
                d= last['dic_rank'][i]
                
                b = str(b)
                c = str(c)
                d = str(d)
               
                if b == 'nan':
                    b = 0
                    if c == 'nan':
                        c =0 
                        if d == 'nan':
                            d=0
                        else:
                            d=float(d)
                    else:
                        c = float(c) 
                        if d == 'nan':
                                d=0
                        else:
                            d= float(d)
                                
                elif c == 'nan':
                        c = 0
                        b = float(b)
                        if d == 'nan':
                            d=0
                        else:
                            d= float(d)
                            
                elif d == 'nan':
                        d = 0
                        b = float(b)
                        c = float(c)
                        
                else: 
                    b = float(b)
                    c = float(c)
                    d = float(d)
                 
                #각 행에 가중치를 설정합니다.
                a1 = a*0.3  #영화 제목
                b1 = b*0.3 # 영화  장르
                c1 = c*0.3 #영화 배우
                d1 = d*0.3 #영화 감독
            
                last_score = a1+b1+c1+d1  #가중치 한값들을 다 더해줍니다.
                            
                last_title.append(title)
                score_box.append(last_score)
            
            final = pd.DataFrame({'title':last_title,
                                'score':score_box})
            final = final.sort_values(by='score', ascending=False)
            final = final.reset_index()
            del final['index']
            #구한 값들을 fianl , df에 넣고 내림차순으로 정렬합니다. 
            pd.options.display.float_format = '{:.2f}'.format
            print('--------------------------------')
            print(final.head(10))
            print('--------------------------------')
            print('{0} 를(을) {1}% 추천합니다'.format(final['title'][0],int(final['score'][0])))
            return print('감사합니다.')
            
            
            

def moviesicker(fmovie):
    if fmovie == 1:
        fmovie = matches[0]
        print(matches[0]+"  검색중")
        print(".\n.\n.")
        recommend(matches[0])
    elif fmovie == 2:
        fmovie = matches[1]
        print(matches[1]+"  검색중")
        print(".\n.\n.")
        recommend(matches[1])
    elif fmovie == 3:
        fmovie = matches[2]
        print(matches[2]+"  검색중")
        print(".\n.\n.")
        recommend(matches[2])
    elif fmovie == 4:
        fmovie = matches[3]
        print(matches[3]+"  검색중")
        print(".\n.\n.")
        recommend(matches[3])
    elif fmovie == 5:
        fmovie = matches[4]
        print(matches[4]+"  검색중")
        print(".\n.\n.")
        recommend(matches[4])
    elif fmovie == 6:
        print('검색실패 : 좀 더 정확히 입력해주세요.')    


#영화 추천기 검색 시작 ----------------------------------------------------
movie_list = df['title'].unique()   
movie = input("영화 제목을 입력하세요   ")
print('1  /   2   /   3  /   4   /  5')
matches = get_close_matches(movie, movie_list, n=5, cutoff=0.2)
print(matches)
print('--------------------------------')
fmovie = input('1~5 중 선택하세요, 없다면 6번')
print('--------------------------------')
fmovie = int(fmovie)

moviesicker(fmovie)     

            
                        
                            
                                
            
                            
        
        
                        
        
                    
                
        
    