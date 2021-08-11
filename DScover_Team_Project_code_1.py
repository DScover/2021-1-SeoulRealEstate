# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# +
# 라이브러리 import
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings(action='ignore')
import datetime

from selenium import webdriver # 크롤링을 위한 라이브러리
from tqdm.notebook import tqdm # 크롤링 진행도를 위한 라이브러리
import time
# -

seoul_data15 = pd.read_csv("서울apt_2015.csv", thousands = ',')
seoul_data16 = pd.read_csv("서울apt_2016.csv", thousands = ',')
seoul_data17 = pd.read_csv("서울apt_2017.csv", thousands = ',')
seoul_data18 = pd.read_csv("서울apt_2018.csv", thousands = ',')
seoul_data19 = pd.read_csv("서울apt_2019.csv", thousands = ',')
seoul_data20 = pd.read_csv("서울apt_2020.csv", thousands = ',')
seoul_data21 = pd.read_csv("서울apt_2021.csv", thousands = ',')

# +
seoul_data = pd.concat([seoul_data15,seoul_data16,seoul_data17,seoul_data18,seoul_data19,seoul_data20,seoul_data21])

seoul_data = seoul_data.drop(['도로명','해제사유발생일'],axis = 1)
seoul_data['구'] = seoul_data.시군구.str.split(' ').str[1]
seoul_data['계약년월'] = pd.to_datetime(seoul_data['계약년월'],format="%Y%m").dt.strftime('%Y-%m')
# -

seoul_mean2 = pd.DataFrame(seoul_data.groupby(['계약년월'])['거래금액(만원)'].mean())
new_seoul_mean2 = seoul_mean2.reset_index()
new_seoul_mean2["상승률"] = new_seoul_mean2["거래금액(만원)"].pct_change()*100


plt.plot(new_seoul_mean2["계약년월"],new_seoul_mean2["거래금액(만원)"],'r')
plt.xticks(['2015-01','2016-01','2017-01','2018-01','2019-01','2020-01','2021-01'])

plt.plot(new_seoul_mean2["계약년월"],new_seoul_mean2["상승률"],'g')
plt.xticks(['2015-01','2016-01','2017-01','2018-01','2019-01','2020-01','2021-01'])

new_seoul_mean2.sort_values(by=['상승률'], axis=0,ascending=False)

# +
df_dc = new_seoul_mean2.sort_values(by=['상승률'], axis=0,ascending=False)["계약년월"][0:4]
df_ac = new_seoul_mean2.sort_values(by=['상승률'], axis=0,ascending=True)["계약년월"][0:4]

df_dc = df_dc.str.split("-", expand = True)
df_ac = df_ac.str.split("-", expand = True)
# -

df_dc # 계약년월을 '-' 기준으로 분리해 사용

df_ac # 계약년월을 '-' 기준으로 분리해 사용

# 크롬 드라이버 실행 후 네이버에서 아무 검색어 입력 후 검색 쿼리주소를 가져와 <br> 해당 쿼리부분에 앞에서 입력한 검색 키워드 문자열 포매팅

# ## 상승률 기준 상위 4개 시기에 대하여 웹크롤링 진행

keyword = '부동산'
total_url_list = []
driver = webdriver.Chrome("chromedriver") # webdriver 위치
for i in range(4):
    url_list = []
    year = df_dc[0].values[i]
    month = df_dc[1].values[i]
    
    m = int(month)
    
    if (m==1)|(m==3)|(m==5)|(m==7)|(m==8)|(m==10)|(m==12): # 몇 월인가에 따라서 해당 월의 마지막 날짜 설정
        end_date = 31
    if (m==4)|(m==6)|(m==9)|(m==11):
        end_date = 30
    if (m==2):
        end_date = 29
        
    for k in range(end_date): # 해당 월의 1일부터 end_date까지 웹크롤링으로 5개씩 기사 링크 추출
        
        if k<10:
            k = '0'+str(k)
        else:
            k = str(k)
            
        a = "https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20170101to20170131&is_sug_officeid=0"
        driver.get(a.format(keyword, year+'.'+month+'.'+ k, year+'.'+month+'.'+ k))
        
        things = driver.find_elements_by_link_text('네이버뉴스')  
    
        try:
            for j in range(5):
                url = things[j].get_attribute('href')  # html 문법의 a태그 href 에서 기사링크 추출
                url_list.append(url)
    
            print(len(url_list)) # 5개 단위로 증가해서 약 150까지 출력이 되어야 정상적으로 진행된 것, 150 이후는 다시 5부터 시작
        except:
            continue
    total_url_list.append(url_list)
driver.close()

print(len(total_url_list)) # 출력값이 4인 경우 총 4개의 시기에 대하여 웹크롤링을 시행한 것으로 정상적으로 진행된 것

for i in range(4):
    
    sdate = df_dc[0].values[i] + '.'  + df_dc[1].values[i]
    file_path = sdate + "_high_url.csv"
    
    print(sdate)
    
    df = pd.DataFrame({'url': total_url_list[i]})
    
    df.to_csv(file_path)

# +
for i in range(4):
    
    dict = {}
    t = []
    b = []
    overlays1 = ".u_cbox_text_wrap"
    sdate = df_dc[0].values[i] + '.'  + df_dc[1].values[i]
    file_path = sdate + "_high_url.csv"
    
    df = pd.read_csv(file_path)
    
    driver = webdriver.Chrome("chromedriver")

# 페이지당 기사 수집
# tqdm을 사용해 진행도 표시

    for i in tqdm(range(len(df['url']))):
    # 드라이버 on    
    
    
        try:      
            driver.get(df['url'][i])
        
            # title에 관하여
            title = driver.find_element_by_css_selector('.tts_head') # css문법에서 class = 'tts_head' 인 tag를 가져옴
            title = title.text
            print(title)
            t.append(title)
        
            # body에 관하여
            body = driver.find_element_by_css_selector('._article_body_contents') # css문법에서 class = '_article_body_contents' 인 tag를 가져옴
            body = body.text
            print(body)
            b.append(body)

        
        
        except:        
            continue
    driver.close()

    dict["title"] = t
    dict["body"] = b
    
    print(len(dict))
    
    article = pd.DataFrame(dict)
    file_path_2 = sdate + "_high_info.csv"
    article.to_csv(file_path_2, encoding = "utf-8-sig")
# -

# ## 상승률 기준 하위 4개 시기에 대하여 웹크롤링 진행

keyword = '부동산'
total_url_list = []
driver = webdriver.Chrome("chromedriver") # webdriver 위치
for i in range(4):
    url_list = []
    year = df_ac[0].values[i]
    month = df_ac[1].values[i]
    
    m = int(month)
    
    if (m==1)|(m==3)|(m==5)|(m==7)|(m==8)|(m==10)|(m==12): # 몇 월인가에 따라서 해당 월의 마지막 날짜 설정
        end_date = 31
    if (m==4)|(m==6)|(m==9)|(m==11):
        end_date = 30
    if (m==2):
        end_date = 29
        
    for k in range(end_date): # 해당 월의 1일부터 end_date까지 웹크롤링으로 5개씩 기사 링크 추출
        
        if k<10:
            k = '0'+str(k)
        else:
            k = str(k)
            
        a = "https://search.naver.com/search.naver?where=news&query={}&sm=tab_opt&sort=0&photo=0&field=0&pd=3&ds={}&de={}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom20170101to20170131&is_sug_officeid=0"
        driver.get(a.format(keyword, year+'.'+month+'.'+ k, year+'.'+month+'.'+ k))
        
        things = driver.find_elements_by_link_text('네이버뉴스')  
    
        try:
            for j in range(5):
                url = things[j].get_attribute('href')  # html 문법의 a태그 href 에서 기사링크 추출
                url_list.append(url)
    
            print(len(url_list)) # 5개 단위로 증가해서 약 150까지 출력이 되어야 정상적으로 진행된 것, 150 이후는 다시 5부터 시작
        except:
            continue
    total_url_list.append(url_list)
driver.close()

print(len(total_url_list)) # 출력값이 4인 경우 총 4개의 시기에 대하여 웹크롤링을 시행한 것으로 정상적으로 진행된 것

for i in range(4):
    
    sdate = df_ac[0].values[i] + '.'  + df_ac[1].values[i]
    file_path = sdate + "_low_url.csv"
    
    print(sdate)
    
    df = pd.DataFrame({'url': total_url_list[i]})
    
    df.to_csv(file_path)

# +
for i in range(4):
    
    dict = {}
    t = []
    b = []
    overlays1 = ".u_cbox_text_wrap"
    sdate = df_ac[0].values[i] + '.'  + df_ac[1].values[i]
    file_path = sdate + "_low_url.csv"
    
    df = pd.read_csv(file_path)
    
    driver = webdriver.Chrome("chromedriver")

# 페이지당 기사 수집
# tqdm을 사용해 진행도 표시

    for i in tqdm(range(len(df['url']))):
    # 드라이버 on    
    
    
        try:      
            driver.get(df['url'][i])
        
            # title에 관하여
            title = driver.find_element_by_css_selector('.tts_head')
            title = title.text
            print(title)
            t.append(title)
        
            # body에 관하여
            body = driver.find_element_by_css_selector('._article_body_contents')
            body = body.text
            print(body)
            b.append(body)

        
        
        except:        
            continue
    driver.close()

    dict["title"] = t
    dict["body"] = b
    
    print(len(dict))
    
    article = pd.DataFrame(dict)
    file_path_2 = sdate + "_low_info.csv"
    article.to_csv(file_path_2, encoding = "utf-8-sig")
