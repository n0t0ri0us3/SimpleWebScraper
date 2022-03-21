# coding: utf-8

from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pytz
import pandas as pd
import itertools
import requests
import random
import time
import xlwt

sayfa = []
tarihler = []
yorumlar = []
to_remove = []

tz = pytz.timezone('Europe/Istanbul')
zaman = datetime.now(tz)

tarih = zaman.strftime("%d.%m.%Y")

session = HTMLSession()

#Sayfa indexleme
for sayfa_sayisi in range(0, 20):
    url = "https://tr.investing.com/equities/afyon-cimento-commentary/" + str(sayfa_sayisi + 1)
    print(url)
    headers = ({'User-Agent': 'Mozilla/5.0 (X11;Ubuntu;Linux_64;rv:82.0) Gecko/20100101 Firefox/82.0'})
    response = session.get(url, headers = headers)
    response.html.render()
    html_kodu = bs(response.html.html, 'html.parser')
    
    yorumlar_veri_raw = html_kodu.find_all('div', class_ = "js-comments-wrapper commentsWrapper")
    
    yorumlar_raw = yorumlar_veri_raw[0]
    
    sayfa = []
    
    for i in range(0, 1000):
        try:
            yorum_raw = yorumlar_raw.find_all('span')[i].text
            sayfa.append(yorum_raw)

        except IndexError:
            break

    cop1 = "Kaydedildi. Kayıtlı Öğeler Kısmını İncele"
    cop2 = "Bu yorum zaten Kayıtlı Öğeler arasında bulunuyor."
    cop3 = "Bildir"
    cop4 = "Önceki cevapları göster"
    cop5 = "Daha fazla göster"
    sayfa = list(filter(None, sayfa))
    
    to_remove = []
    
    for i in range(0, len(sayfa)):
        try:
            if cop1 in sayfa[i]: to_remove.append(i)
            if cop2 in sayfa[i]: to_remove.append(i)
            if cop3 in sayfa[i]: to_remove.append(i)
            if cop4 in sayfa[i]: to_remove.append(i)
            if cop5 in sayfa[i]:
                if "...Daha fazla göster" in sayfa[i]:
                    sayfa[i] = sayfa[i][:-20]
                    
                else:
                    to_remove.append(i)

        except IndexError:
            break

    k = 0
    
    for i in range(0, len(to_remove)):
        sayfa.remove(sayfa[to_remove[i] - k])
        k += 1
        
    for i in range(0, len(sayfa)):
        if((i % 5) == 1): tarihler.append(sayfa[i])
        elif((i % 5) == 2): yorumlar.append(sayfa[i])
            
    for i in range(0, len(tarihler)):
        if ("önce") in tarihler[i]:
            tarihler[i] = tarih 
    
    time.sleep(1)
    print("{}. sayfa index'lendi".format(sayfa_sayisi + 1))
    
print("Yorumların tamamı başarıyla çekildi!")
    
sutunlar = ['Tarih', 'Yorum']

yorumlar_df = pd.DataFrame({
                            'Yorum': yorumlar,
                            'Tarih': tarihler})[sutunlar]

yorumlar_df.to_excel('afyon_cimento_yorumlari.xls')

