#_*_coding:utf-8_*_
import xlwt
import chardet
import MySQLdb


file1='/media/liang/3804CCCA04CC8C76/GSlinshi/20170609.txt'
connect=MySQLdb.connect(host='127.0.0.1',user='root',passwd='asd123456',db='WHNTxtToExcel',charset='utf8')
cursor1=connect.cursor()

with open(file1,'r+') as fl:
    datalines=fl.readlines()
    for i in datalines:
        try:
            oneline= i.split('-|-')
            fromwhere= oneline[0]
            content=oneline[2].replace('"',"-")
            commentNum=int(oneline[3])
            publishtime=oneline[4]


            print 111
            # print chardet.detect(fromwhere)
            # print chardet.detect(content)
            # # print chardet.detect(commentNum)
            # print chardet.detect(publishtime)

            sqlWHN='INSERT INTO WHNTxtToExcel.DENGDENG (fromwhere,content,commentNum,publishtime) VALUE ("%s","%s","%d","%s")'%(fromwhere,content,commentNum,publishtime)
            print sqlWHN
            cursor1.execute(sqlWHN)
            connect.commit()
        except Exception as e:
            print e