import json
import os
from flask import url_for

def response(data, err = 0):
	return json.dumps({
		'data': data,
		'err': err
	}, indent = 2, ensure_ascii = False)

class BillController:
	billsList = []
	inBillUsers = []

	def createBill(self, ctx):
		ctxBody = ctx.form
		user = {
			'userId': ctxBody['userId'],
			'billId': ctxBody['billId'],
			'name': ctxBody['name'],
			'avatar': ctxBody['avatar']
		}
		bill = {
			'billId': ctxBody['billId'],
			'from': ctxBody['from'],
			'to': ctxBody['to'],
			'time': ctxBody['time'],
			'members': [user]
		}
		if ctxBody['userId'] in [item['userId'] for item in self.inBillUsers]:
			return response({
				'errMsg': '用户已经在拼单中！'
			}, 1)
		self.billsList.append(bill)
		self.inBillUsers.append(user)
		return response({
			'billsList': self.billsList,
			'inBillUsers': self.inBillUsers
		})

	def joinBill(self, ctx):
		ctxBody = ctx.form
		billId = ctxBody['billId']
		user = {
			'userId': ctxBody['userId'],
			'name': ctxBody['name'],
			'avatar': ctxBody['avatar'],
			'billId': ctxBody['billId']
		}
		if ctxBody['userId'] in [item['userId'] for item in self.inBillUsers]:
			return response({
				'errMsg': '用户已经在拼单中！'
			}, 1)
		theBill = [item for item in self.billsList if item['billId'] == billId]
		if not theBill:
			return response({
				'errMsg': '拼单不存在'
			}, 1)
		theBill[0]['members'].append(user)
		self.inBillUsers.append(user)
		return response({
			'billsList': self.billsList,
			'inBillUsers': self.inBillUsers
		})

	def leaveBill(self, ctx):
		ctxBody = ctx.form
		billId = ctxBody['billId']
		userId = ctxBody['userId']
		indexOfUser = [i for i, member in enumerate(self.inBillUsers) if member['userId'] == userId][0]
		indexOfTheBill = [i for i, bill in enumerate(self.billsList) if bill['billId'] == billId][0]
		indexOfUserInBill = [i for i, member in enumerate(self.billsList[indexOfTheBill]['members']) if member['userId'] == userId][0]
		# 删除拼单里面的该用户
		self.billsList[indexOfTheBill]['members'].pop(indexOfUserInBill)
		# 删除用户列表里面的该用户
		self.inBillUsers.pop(indexOfUser)
		# 如果拼单里面用户为空，则直接删除这笔拼单
		if len(self.billsList[indexOfTheBill]['members']) == 0:
			imgPath = './imgs/' + self.billsList[indexOfTheBill]['img'].split('/getImg')[1]
			if os.path.exists(imgPath):
				os.remove(imgPath)
			self.billsList.pop(indexOfTheBill)
		return response({
			'billsList': self.billsList,
			'inBillUsers': self.inBillUsers
		})

	def getBill(self, ctx):
		ctxBody = ctx.form
		billId = ctxBody['billId']
		try: 
			return response([item for item in self.billsList if item['billId'] == billId][0])
		except IndexError:
			return response({
				'errMsg': '拼单不存在！',
				'billsList': self.billsList,
			}, 1)

	def inBill(self, ctx):
		ctxBody = ctx.form
		userId = ctxBody['userId']
		if ctxBody['userId'] in [item['userId'] for item in self.inBillUsers]:
			return response({
				'inBill': [item for item in self.inBillUsers if ctxBody['userId'] == item['userId']][0],
				'billsList': self.billsList,
				'inBillUsers': self.inBillUsers
			})
		return response({
			'inBill': False,
			'billsList': self.billsList,
			'inBillUsers': self.inBillUsers
		})

	def uploadImg(self, ctx):
		billId = ctx.form['billId']
		file = ctx.files['file']
		filename = file.filename
		file.save(os.path.join('./imgs', filename))
		# 把图片信息挂载到对应的拼单
		indexOfTheBill = [i for i, bill in enumerate(self.billsList) if bill['billId'] == billId][0]
		self.billsList[indexOfTheBill]['img'] = url_for('getImg', filename=filename)
		return response({
			'billsList': self.billsList
		})
		