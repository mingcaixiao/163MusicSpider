import json
import random
import time
from concurrent.futures.thread import ThreadPoolExecutor

import requests
import atexit
import xlwt
import numpy as np

user_agents=['Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',\
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',\
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',\
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',\
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',\
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',\
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',\
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',\
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',\
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',\
    'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',\
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; TencentTraveler 4.0; .NET CLR 2.0.50727)',\
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',\
    'Mozilla/5.0 (compatible; Yahoo! Slurp;http://help.yahoo.com/help/us/ysearch/slurp)',\
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gcko) Chrome/50.0.2661.102 Safari/537.36; 360Spider'
]




#爬取网站内容
def getHTMLText(url):
    #伪造浏览器请求头
    headers = {'User-Agent': random.choice(user_agents)}
    try:
        r=requests.get(url=url,headers=headers,timeout=0.25)
        r.raise_for_status()
        r.encoding='UTF-8'
        return r.text
    except:
        print('爬取失败!'+'   重新爬取')



#写入excel文件
def write_excel(filename,data):
    path='./data/'+filename
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("comment")
    #转化为array
    array=np.array(data)
    #读取列表的行数和列数
    [r,c]=array.shape
    sheet.write(0,0,'id')
    sheet.write(0,1,'评论时间')
    sheet.write(0,2,'评论')
    for  row in range(r):
        for column in range(c):
            sheet.write(row+1,column,array[row,column])
    workbook.save(path)
#获取某一页的评论值、用户id和评论时间
def get_comment(url):
    try:
        #time.sleep(random.uniform(0.1,1))#延迟执行
        response=getHTMLText(url)#json格式
        dic=json.loads(response) #json格式转为dict
        for i in range(len(dic['comments'])):
            #评论
            comment_info = []
            comment=dic['comments'][i]['content']
            id=dic['comments'][i]['user']['userId']#id
            comment_time=dic['comments'][i]['time']#时间戳
            comment_info.append(id)
            comment_info.append(comment_time)
            comment_info.append(comment)
            music_comment.append(comment_info)#存入列表
    except Exception as e:
        print(repr(e))



#存储网易云评论的列表
music_comment=[]
begin=time.time()
base_url="http://music.163.com/api/v1/resource/comments/R_SO_4_436514312"

if __name__=='__main__':
    #异常退出时保存文件
    atexit.register(write_excel,filename='{}评论.xls'.format(time.time()),data=music_comment)
    total=20000 #评论数
    #获取第一页的评论和该歌曲的评论总数
    while True:
        try:
            response=getHTMLText(base_url)
            first=json.loads(response)
            #获取评论总数
            total_text=first['total']
            total=int(total_text)
            print("评论总数为： {}".format(total))
            #获取第一页信息
            get_comment(base_url)
            break
        except Exception as e:
            print(repr(e))

    # 线程池
    # pool=ThreadPoolExecutor(4)total//
    #循环遍历获取后面的评论
    for i in range(total//10,total//10+1):
        url=base_url+'?'+'limits=20&offset={}'.format(20*i)
        get_comment(url)
        time.sleep(random.uniform(0,2))
    end=time.time()
    print('抓取的评论数量为：{}'.format(len(music_comment)))
    # #写入txt
    # text_save('{}评论.txt'.format(time.time()),music_comment)
    #写入excel
    write_excel('{}评论.xls'.format(time.time()),music_comment)

    print("爬虫用时{:.2f}秒".format(end-begin))