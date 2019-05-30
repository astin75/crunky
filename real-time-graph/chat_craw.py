# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:06:01 2019

@author: A
"""

#project  Sand castle

import pandas as pd
import re, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome('driver/chromedriver')
driver.get("https://www.youtube.com/live_chat?is_popout=1&v=W9jr3QypVCg")

driver2 = webdriver.Chrome('driver/chromedriver')
driver2.get("https://www.twitch.tv/popout/zilioner/chat?popout=")

df = pd.DataFrame({'text':box3})
df.to_csv('chattest2.csv', index=False)  
        
df1 = pd.read_csv('chattest1.csv')        

len(df1)
df1

sandbox(1,1000)

#  모래알 모으기 
def sandbox(a,b):
    box3 = []
    for i in range(a,b):
        
        try:
            bb = driver2.find_element_by_xpath('''//*[@id="root"]/div/div[1]/div/div/section/div/div[2]/div[2]/div[3]/div/div/div[1]/span[4]'''   )
            a1=a2=a3=a4=a5=a6= bb.text
            
            a2 = a2+'2'
            a3 = a3+'3'
            a4 = a4+'4'
            a5 = a5+'5'
            a6 = a6+'5'
            box3.append(a1)
            box3.append(a2)
            box3.append(a3)
            box3.append(a4)
            box3.append(a5)
            box3.append(a6)
            print(a1)
    
        except:
            print('haha %d' %i)
        
        if len(box3) >= 5:
            df = pd.DataFrame({'text':box3,
                               'text1':box3,
                               'text2':box3})
            df.to_csv('chattest1.csv', index=False) 
            
            #if len(box3) >= 10000:
             #   break   
        
#모래 사장~
                
len(box3)            

            
        bb = driver2.find_element_by_xpath('''//*[@id="root"]/div/div[1]/div/div/section/div/div[2]/div[2]/div[3]/div/div/div[1]/span[4]'''  )
        a1=a2=a3=a4=a5= bb.text
        a1 = a1+'1'
        
        a1

    


