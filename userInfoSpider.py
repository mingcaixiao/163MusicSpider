import musicCommentsSpider as c
import random
import json
import xlrd
import xlwt
import numpy as np
import time

def get_user_info(url):
    #伪造浏览器请求头
    headers = {'User-Agent': random.choice(c.user_agents)}
    user_info=[]
    try:
        proxies=c.get_proxy()
        response=c.getHTMLText(url,proxies)
        dic=json.loads(response) #json格式转为dict
        #获取用户生日、使用时间、城市代码、省份代码、性别和等级
        profile=dic['profile']
        birthday=profile['birthday']
        createTime=dic['createDays']
        city=profile['city']
        province=profile['province']
        gender=profile['gender']
        vipLevel=dic['level']
        #单个用户的信息
        user_info.append(birthday)
        user_info.append(createTime)
        user_info.append(city)
        user_info.append(province)
        user_info.append(gender)
        user_info.append(vipLevel)
        return user_info
    except Exception as e:
        print(repr(e))


#从文件中读取用户id
def read_id():
    wb=xlrd.open_workbook("./data/成都评论.xls")
    sheet=wb.sheets()[0]
    rows=sheet.nrows #获取行数
    id=[]
    for i in range(1,rows):
        cell=sheet.cell_value(i,0)#id在第一列
        id.append(cell)
    return id

#写入excel文件
def write_to_excel(filename,data):
    path='./data/'+filename
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("comment")
    #转化为array
    array=np.array(data)
    #读取列表的行数和列数
    [r,c]=array.shape
    sheet.write(0,0,'用户生日')
    sheet.write(0,1,'使用时间')
    sheet.write(0,2,'城市代码')
    sheet.write(0,3,'省份代码')
    sheet.write(0,4,'性别')
    sheet.write(0,5,'等级')
    for  row in range(r):
        for column in range(c):
            sheet.write(row+1,column,str(array[row,column]))
    workbook.save(path)

if __name__=='__main__':
    id=read_id()#用户id
    #存储用户信息的列表
    users_info=[]
    begin=time.time()
    for i in range(len(id)):
        try:
            #用户信息API
            url="https://music.163.com/api/v1/user/detail/"+str(id[i])
            user_info=get_user_info(url)
            #判断user_info是否为空
            if user_info:
                users_info.append(user_info)
            else:
                #重新爬取这一页内容
                i=i-1
        except Exception as e:
            print(repr(e))
    #存储信息
    end=time.time()
    print("爬虫用时{:.2f}秒".format(end-begin))
    write_to_excel('{}用户信息1.xls'.format(time.time()),users_info)