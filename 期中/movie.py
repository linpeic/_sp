import requests
from bs4 import BeautifulSoup
import threading
# import time
# from googletrans import Translator #會有因為一直被請求而當掉的問題，所以換一個翻譯套件
from deep_translator import GoogleTranslator

# translator = GoogleTranslator()
# 目標 爬完前15名的電影後，列出詳細資訊
movie_list = []
score_list = []
year_list=[]
time_list=[]
all_list = []
link_list = []
click_list=[]
# 詳細介紹相關
#會有順序錯亂問題
# class_list = []
# info_list = []
# tran_list = []
main_url = "https://www.imdb.com"
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
#現在很容易被擋(以為是機器人)，所以在爬的時候加入這個會讓網頁當成真正使用者在使用
headers = {
    "Cookie": "session-id=130-9659096-1679810; session-id-time=2082787201l; csm-hit=tb:s-C4RTEK426QYW1M54A0QY|1746699169976&t:1746699170667&adb:adblk_no; ad-oo=0; ci=eyJpc0dkcHIiOmZhbHNlfQ",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"}
# time.sleep(2)
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
allmovies=soup.select("div.sc-995e3276-1.jziSZL.cli-parent.li-compact")[:15]
for allmovie in allmovies:
    title = allmovie.select_one("h3").text.strip()
    movie_list.append("Top"+title)
    score =allmovie.select_one("span.ipc-rating-star--rating").text.strip()
    score_list.append("評分："+score)
    time =allmovie.select("span.sc-4b408797-8.iurwGb.cli-title-metadata-item")
    year=time[0].text.strip()
    long=time[1].text.strip()
    year_list.append("年分："+year)
    time_list.append("片長："+long)
    link=allmovie.select_one("a.ipc-title-link-wrapper").get("href")
    link_list.append(link)
    href=main_url+link
    click_list.append(href)
# print(movie_list)
# print(score_list)
# print(year_list)
# all_list = list(zip(movie_list, score_list, year_list))
# print(all_list)
# print(link_list)
# print(click_list) #['https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1', ...]

#先寫沒有thread的版本
# for urlin in click_list:
#     response = requests.get(urlin, headers=headers)
#     soup = BeautifulSoup(response.text, "html.parser")
#     # findclasses=soup.select("div.ipc-chip-list__scroller")
#     findclasses=soup.select("a.ipc-chip.ipc-chip--on-baseAlt span.ipc-chip__text")
#     fcitem=[classes.text.strip() for classes in findclasses]
#     fc=",".join(fcitem) #Epic,Period Drama,Prison Drama,Drama
#     class_list.append("電影分類："+fc)
#     information=soup.select("span.sc-d6f3b755-0.erEDdh")
#     for info in information:
#         introduction=info.text.strip()
#         translation = translator.translate(introduction, dest='zh-tw').text.replace("\u200b","")
#         info_list.append(f"原文簡介：{introduction}翻譯簡介：{translation}")
#     # print(translation)
# # print(class_list)
# # print(info_list)
# all_list = list(zip(movie_list, score_list, year_list,class_list,info_list))
# print(all_list)

#執行每一部電影的詳細爬蟲
#要確保順序一致，因為原本使用class=[]會發生電影名稱、類別、簡介對不起來的問題
class_list = [None] * len(click_list)
star_list=[None] * len(click_list)
info_list = [None] * len(click_list)
tran_list = [None] * len(click_list)
threads=[]
def movie_detail(index,urlin):
    response = requests.get(urlin, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    superstars = soup.select("div.ipc-metadata-list-item__content-container ul.ipc-inline-list.ipc-inline-list--show-dividers.ipc-inline-list--inline.ipc-metadata-list-item__list-content.baseAlt li.ipc-inline-list__item a.ipc-metadata-list-item__list-content-item.ipc-metadata-list-item__list-content-item--link")
    # print(superstars)
    moviestar=[superstar.text.strip() for superstar in superstars]
    #Frank Darabont,Stephen King,Frank Darabont,Tim Robbins,Morgan Freeman,Bob Gunton,Frank Darabont,Stephen King,Frank Darabont,Tim Robbins,Morgan Freeman,Bob Gunton
    norepeat=list(dict.fromkeys(moviestar))#去除重複的人員
    ms=",".join(norepeat)
    findclasses = soup.select("a.ipc-chip.ipc-chip--on-baseAlt span.ipc-chip__text")
    fcitem=[classes.text.strip() for classes in findclasses] #把所有相同類型的資料(爬出來的)都丟入list中
    fc=",".join(fcitem) #Epic,Period Drama,Prison Drama,Drama
    # class_list.append("電影分類："+fc)
    information = soup.select("span.sc-d6f3b755-0.erEDdh")
    for info in information:
        introduction=info.text.strip()
        # translation = translator.translate(introduction, dest='zh-tw').text.replace("\u200b","")
        translation = GoogleTranslator(source='auto', target='zh-TW').translate(introduction)
        # info_list.append("原文簡介："+introduction)
        # tran_list.append("翻譯簡介："+translation)
    star_list[index]="參與人員："+ms
    class_list[index]="電影類別："+fc
    info_list[index]="原文簡介："+introduction
    tran_list[index]="翻譯簡介："+translation
for index,urlin in enumerate(click_list):
    #enumerate取得index跟內容
    thread=threading.Thread(target=movie_detail,args=(index,urlin))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
# print(class_list)
# print(info_list)
# print(tran_list)
all_list = list(zip(movie_list, score_list, year_list,time_list,star_list,class_list,info_list,tran_list))
# print(all_list)

for item in all_list:
    print("\n".join(item)) #換行連接
    print("." * 150)