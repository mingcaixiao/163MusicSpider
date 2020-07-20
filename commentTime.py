import xlrd
import time
import xlwt
import numpy as np

#获取用户信息中的某一个字段
def get_data(column):
    wb=xlrd.open_workbook("./data/成都评论.xls")
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

#获取评论时间
    commentTime=[]#转化后的时间
    comment=get_data(2)#获取时间戳
    for i in range(len(comment)):
        if int(comment[i])>0:
            #将时间戳转化为localtime
            localtime=time.localtime(int(comment[i])//1000)#13位时间戳转成10位的
            #转换成新的时间格式(2016-05-09)
            c1 = time.strftime("%Y-%m-%d",localtime)
            commentTime.append(c1)
    write_to_excel(commentTime,'评论时间.xls')