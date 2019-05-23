#!/usr/bin/env python
#encoding:utf-8
from __future__ import division #是运算采用浮点除法，即2/3=0.6666。
import tornado.web
import tornado.gen 
from base import BaseHandler
import jinja2
from jinja2 import Environment, FileSystemLoader
import os
#操作Excel
import xlrd #读
import xlwt #写
from xlutils.copy import copy #改
from io import BytesIO
def read_excel(filepath,fileName):
    # 打开文件
	workbook = xlrd.open_workbook(filepath)
	# 获取所有sheet
	# print workbook.sheet_names()
	# [u'sheet1', u'sheet2']
	#sheet1_name = workbook.sheet_names()[0]
	# 根据sheet索引或者名称获取sheet内容
	sheet1 = workbook.sheet_by_index(0) # sheet索引从0开始

	# sheet的名称，行数，列数
	# print sheet1.name,sheet1.nrows,sheet1.ncols
	# # 获取整行和整列的值（数组）
	# rows = sheet1.row_values(3) # 获取第四行内容
	# cols = sheet1.col_values(sheet1.ncols-1) # 获取最后一列内容
	# print rows
	# print cols
	coin_list = sheet1.col_values(sheet1.ncols-1)[4:] # 获取所有成绩
	hight_coin=coin_list[0]
	low_coin=coin_list[len(coin_list)-1]
	total_peple=len(coin_list)
	Y_1=coin_list[int(total_peple*0.15)-1]
	Y_2=coin_list[int(total_peple*0.5)-1]
	Y_3=coin_list[int(total_peple*0.85)-1]
	Y_4=coin_list[int(total_peple*0.98)-1]
	# # 获取单元格内容
	# print sheet1.cell(1,0).value.encode('utf-8')
	# print sheet1.cell_value(1,0).encode('utf-8')
	# print sheet1.row(1)[0].value.encode('utf-8')
    
	# # 获取单元格内容的数据类型
	# print sheet1.cell(1,0).ctype

	wb=copy(workbook) #复制一份，用作修改
	#修改
	ws=wb.get_sheet(0)
	ws.write(3,sheet1.ncols,label='转换成绩'.decode("utf-8"))
	try:
		for index,one in enumerate(coin_list):
			X=0
			if one >= Y_1:
				Y2=hight_coin
				Y1=Y_1
				X2=100
				X1=86
				Y=one
			elif one >= Y_2:
				Y2=Y_1
				Y1=Y_2
				X2=85
				X1=71
				Y=one
			elif one>= Y_3:
				Y2=Y_2
				Y1=Y_3
				X2=70
				X1=56
				Y=one
			elif one>= Y_4:
				Y2=Y_3
				Y1=Y_4
				X2=55
				X1=41
				Y=one
			else:
				Y2=Y_4
				Y1=low_coin
				X2=40
				X1=30
				Y=one
			X=round(Y*(X2-X1)/(Y2-Y1)+(X1*Y2-X2*Y1)/(Y2-Y1),1)
			ws.write(4+index,sheet1.ncols,X)
	except Exception as e:
		print e
	#保存修改
	try:
		wb.save(filepath)
	except Exception as e:
		print e
class IndexHandler(BaseHandler):
	@tornado.web.asynchronous
	@tornado.gen.coroutine
	def get(self):
		env = Environment(loader=FileSystemLoader("templates"))
		template = env.get_template("01-index1.html")
		page = template.render(
		)
		self.write(page)
		self.finish()
	def post(self):
		file_list=[]
		filepath=''
		fileName=''
		result=''
		upload_path=os.path.join(os.path.dirname(os.path.dirname(__file__)),'files')  #文件的暂存路径 
		if not os.path.exists(upload_path):
			os.makedirs(upload_path)
		try:
			for root,dirs,files in os.walk(upload_path):
				for filename in files:
					file_list.append(filename) #取该路径下所有文件(用户名_问卷名_量表名_时间戳.pdf)
				for one in file_list:
					os.remove(os.path.join(upload_path,one))
		except Exception as e:
			pass
		try:
			pdffile=self.request.files.get("file")   #提取表单中‘name’为‘file’的文件元数据
			for pdf in pdffile:
				filepath=os.path.join(upload_path,pdf['filename'].decode("utf-8"))
				fileName=pdf['filename'].decode("utf-8")
				#以wb+方式打开文件，没有则创建该文件
				with open(filepath,'wb+') as up:      #有些文件需要以二进制的形式存储，实际中可以更改  
					up.write(pdf['body'])
			read_excel(filepath,fileName)
		except Exception as e:
			pass
		data={"error":0,"data":fileName}
		self.write(data)
		self.finish()

            
