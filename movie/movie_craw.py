# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 01:55:49 2019

@author: Administrator1
"""

#refer.. https://movie.naver.com/movie/point/af/list.nhn?st=nickname&target=after&sword=15480284
#package
import pandas as pd
import os, sys
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from difflib import SequenceMatcher, get_close_matches

box1 = []
box2 = []
box3 = []
box4 = []
dirc1 = []
dirc2 = []
act1 = []
act2 = []
act3 = []
gen1 = []
gen2 = []
gen3 = [] 



#영화 추천기 검색 시작 ----------------------------------------------------


#---------------------------------------------------------------


scv(130000,140000)



def scv(a,b):

    for i in range(a,b):

        page1 = urlopen("https://movie.naver.com/movie/point/af/list.nhn?st=nickname&sword=%d&target=after&page=1" %i)
        page1
        soup1 = BeautifulSoup(page1)
        
        if len(soup1) == 2: #페이지가 삭제 되었다면
            none = 1

            print("none")
            


        else:
                print(i)
                bb = soup1.find('tbody')             #페이지에 평점 개수 추적
                count1 = len(bb.find_all('tr'))
                if count1 == 10:
                    userid = soup1.find_all('h5')[0].text #아이디


                    userid1 = re.split("\n",userid)[0]   #유저아이디정제
                   # userid1 = userid1 +'%s' %i


                    for n in range(0,count1):
                        moviet = soup1.find_all('td', 'title')[n].a.string #영화제목
                        moviep = soup1.find_all('td', 'point')[n].text #평점
                        moviei = soup1.find_all('td', 'title')[n].a['href'] #영화 고유 번호_href
                        moviei1 = int(re.findall('\d+',moviei)[0]) #href 에서 번호만 추출
                        
                        page2 = urlopen("https://movie.naver.com/movie/bi/mi/photoViewPopup.nhn?movieCode=%d" % moviei1)
                        soup2 = BeautifulSoup(page2)
                        

                        try: 
                            
                                mvimg = soup2.find_all('img')[0]['src']
                                
                        except IndexError:
                            
                               print('shhot')
                               mvimg = None
                                               

                        print(moviet)
                        

                        
                        page3 = urlopen("https://movie.naver.com/movie/bi/mi/basic.nhn?code=%d" % moviei1)
                        soup3 = BeautifulSoup(page3)
                        
                        
                        
                        if len(soup3.find_all('div','choice_movie')) >= 1:
                            print('old')

                                
                        
                        else:
                            #감독 추가 
                            print('new')
                            try:
                                
                                dirc = soup3.find_all('dl')[0].dd
                                d_c = len(dirc.find_all('a'))
                                act = soup3.find_all('dl')[1].dd
                                a_c = len(act.find_all('a'))
                                genre = soup3.find_all('dl')[2].dd
                                genre = genre.find_all('span')[0]
                                g_c = len(genre.find_all('a'))
                                box1.append(userid1)
                                box2.append(moviet)
                                moviep = int(moviep)
                                box3.append(moviep)
                                box4.append(mvimg)
                                
                                
                                if d_c == 1:
                                    a = dirc.find_all('a')[0].text
                                    dirc1.append(a)
                                    dirc2.append(None)
                                elif d_c ==2:
                                    a = dirc.find_all('a')[0].text
                                    a1 = dirc.find_all('a')[1].text
                                    dirc1.append(a)
                                    dirc2.append(a1)
                                else:
                                    dirc1.append(None)
                                    dirc2.append(None)
                                  
                                
                                #배우추가
                                
                                if a_c ==1:
                                    a = act.find_all('a')[0].text
                                    act1.append(a)
                                    act2.append(None)
                                    act3.append(None)
                                    
                                elif a_c ==2:
                                    a1 = act.find_all('a')[0].text
                                    a2 = act.find_all('a')[1].text
                                    act1.append(a1)
                                    act2.append(a2)
                                    act3.append(None)
                                    
                                elif a_c == 3:
                                    a1 = act.find_all('a')[0].text
                                    a2 = act.find_all('a')[1].text
                                    a3 = act.find_all('a')[2].text
                                    act1.append(a1)
                                    act2.append(a2)
                                    act3.append(a3)
                                
                                else:
                                    act1.append(None)
                                    act2.append(None)
                                    act3.append(None)
                                    
                                #장르 추가    

                                
                                if g_c == 1:
                                    a1 = genre.find_all('a')[0].text
                                    gen1.append(a1)
                                    gen2.append(None)
                                    gen3.append(None)
                                    
                                elif g_c == 2:
                                    a1 = genre.find_all('a')[0].text
                                    a2 = genre.find_all('a')[1].text
                                    gen1.append(a1)
                                    gen2.append(a2)
                                    gen3.append(None)
        
                                elif g_c == 2:
                                    a1 = genre.find_all('a')[0].text
                                    a2 = genre.find_all('a')[1].text
                                    a3 = genre.find_all('a')[2].text
                                    gen1.append(a1)
                                    gen2.append(a2)
                                    gen3.append(a3)
                                
                                else:
                                    a1 = genre.find_all('a')[0].text
                                    a2 = genre.find_all('a')[1].text
                                    a3 = genre.find_all('a')[2].text
                                    gen1.append(a1)
                                    gen2.append(a2)
                                    gen3.append(a3)
                                

                            except:
                                print(';')
#--------------------------------------------------------------------------------

    # except 제거하기
    box44 = []
    for i in box4:
        if i != 1:
            box44.append(i)
            print(i)
    # except 제거하기
    df = pd.DataFrame({ # DF 만들기
                    'userid':box1,
                   'title':box2,
                   'point':box3,
                   'pn':box44,
                   'dirc1':dirc1,
                   'dirc2':dirc2,
                   'act1':act1,
                   'act2':act2,
                   'act3':act3,
                   'gen1':gen1,
                   'gen2':gen2,
                   'gen3':gen3})
    



 #---------------------------------------------------------------------------   

    

df.to_csv('movie130000.csv', index=False, encoding='euc-kr')
