import xlrd
import time
import matplotlib.pyplot as plt
import xlwt
import numpy as np
#获取邮政编码以及对应的省市和城市
def get_stamp(path):
    wb=xlrd.open_workbook(path)
    sheet=wb.sheets()[0]
    stamp_dic=dict()#邮政编码对应字典
    for row in range(1,sheet.nrows):
            postCode=int(sheet.cell_value(row,0))#编码在第一列
            place=sheet.cell_value(row,1)#地点在第二列
            stamp_dic[postCode]=place
    return stamp_dic

#获取用户信息中的某一个字段
def get_data(column):
    wb=xlrd.open_workbook("./data/用户信息.xls")
    sheet=wb.sheets()[0]
    rows=sheet.nrows #获取行数
    list=[]
    for i in range(1,rows):
        cell=sheet.cell_value(i,column-1)
        list.append(cell)
    return list

#将修改后的字段写入excel中
def write_to_excel(data,filename):
    path='./data/'+filename
    workbook=xlwt.Workbook()
    sheet=workbook.add_sheet("data")
    #转化为array
    array=np.array(data)
    sheet.write(0,0,filename[0:4])
    #读取列表的行数和列数
    for  row in range(1,len(array)):
            sheet.write(row,0,array[row])
    workbook.save(path)

if __name__=='__main__':
    stamp_dic=dict()#邮政编码字典
    stamp_dic=get_stamp("./data/邮政编码对应表.xlsx")
    #生日
    birthday=get_data(1)
    ages=[]#年龄
    #计算年龄
    for i in range(len(birthday)):
        #负值为错误数据
        if int(birthday[i])>0:
            #将时间戳转化为localtime
            localtime=time.localtime(int(birthday[i])//1000)#13位时间戳转成10位的
            #转换成新的时间格式(2016-05-09)
            age = time.strftime("%Y-%m-%d",localtime)[0:4]
            if(int(age)<2019):
                ages.append(2019-int(age))
    #将年龄分为3段：0-18，19—30，30-40
    first=second=third=0
    for i in range(len(ages)):
        if int(ages[i])<=18:
            first+=1
        elif int(ages[i])<=30:
            second+=1
        else :
            third+=1

    #绘制年龄饼图

    #标签
    age_label=['0-18','19—30','>30']
    age_list=[first,second,third]
    plt.pie(age_list,labels=age_label,explode=[0, 0.05, 0],autopct='%.1f%%')
    plt.axis("equal")    # 设置横轴和纵轴大小相等，这样饼才是圆的
    plt.legend()
    plt.show()

    #将账号创建时间转换后写入excel
    createTime=[]#转化后的时间
    create=get_data(2)#获取时间戳
    for i in range(len(create)):
        if int(create[i])>0:
            #将时间戳转化为localtime
            localtime=time.localtime(int(create[i])//1000)#13位时间戳转成10位的
            #转换成新的时间格式(2016-05-09)
            c1 = time.strftime("%Y-%m-%d",localtime)
            createTime.append(c1)
    write_to_excel(createTime,'账号创建时间.xls')

    #将城市和省份代码转化为名称存入excel
    cityName=[]
    provinceName=[]
    city=get_data(3)#城市代码
    province=get_data(4)#省份代码
    for i in range(len(city)):
        #邮编代码长度等于6或者代码在邮编的字典中
        if len(city[i])==6 and (int(city[i]) in stamp_dic.keys()) and int(province[i]) in stamp_dic.keys() :
            cityName.append(stamp_dic[int(city[i])])
            provinceName.append(stamp_dic[int(province[i])])
    #写入excel
    write_to_excel(cityName,'城市名称.xls')
    write_to_excel(provinceName,'省份名称.xls')