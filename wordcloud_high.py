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
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from konlpy.tag import Okt
from PIL import Image
import numpy as np 
from wordcloud import ImageColorGenerator
# -

data1709 = pd.read_csv('2017.09_high_info.csv')
data1807 = pd.read_csv('2018.07_high_info.csv')
data1903 = pd.read_csv('2019.03_high_info.csv')
data2005 = pd.read_csv('2020.05_high_info.csv')

text1 = ''.join(v for v in data1709['title'])
text2 = ''.join(v for v in data1807['title'])
text3 = ''.join(v for v in data1903['title'])
text4 = ''.join(v for v in data2005['title'])

# +
text1 = text1.replace('부동산', '')
text1 = text1.replace('.','')

text2 = text2.replace('부동산', '')
text2 = text2.replace('.','')

text3 = text3.replace('부동산', '')
text3 = text3.replace('.','')

text4 = text4.replace('부동산', '')
text4 = text4.replace('.','')
# -

image_example = np.array(Image.open('koreaMap.jpg'))
mask = np.array(image_example)
image_colors = ImageColorGenerator(image_example)

wordcloud = WordCloud(font_path = 'NanumSquareR.ttf',
                      max_font_size = 100,
                      random_state = 42,
                      mask = mask, 
                      max_words=150, 
                      background_color = 'white',
                      width=mask.shape[1], 
                      height=mask.shape[0]).generate(text1)

plt.figure(figsize=(12,15))
plt.axis('off')
plt.imshow(wordcloud, interpolation='bilinear') 
plt.show()

# +
wordcloud = WordCloud(font_path = 'NanumSquareR.ttf', 
                      max_font_size = 100,
                      random_state = 42,
                      mask = mask, 
                      max_words=150, 
                      background_color = 'white',
                      width=mask.shape[1], 
                      height=mask.shape[0]).generate(text2)

plt.figure(figsize=(12,15))
plt.axis('off')
plt.imshow(wordcloud, interpolation='bilinear') 
plt.show()

# +
wordcloud = WordCloud(font_path = 'C:/Users/hyang/Desktop/font/NanumSquareR.ttf', 
                      max_font_size = 100,
                      random_state = 42,
                      mask = mask, 
                      max_words=150, 
                      background_color = 'white',
                      width=mask.shape[1], 
                      height=mask.shape[0]).generate(text3)

plt.figure(figsize=(12,15))
plt.axis('off')
plt.imshow(wordcloud, interpolation='bilinear') 
plt.show()

# +
wordcloud = WordCloud(font_path = 'NanumSquareR.ttf', 
                      max_font_size = 100,
                      random_state = 42,
                      mask = mask, 
                      max_words=150, 
                      background_color = 'white',
                      width=mask.shape[1], 
                      height=mask.shape[0]).generate(text4)

plt.figure(figsize=(12,15))
plt.axis('off')
plt.imshow(wordcloud, interpolation='bilinear') 
plt.show()
# -




