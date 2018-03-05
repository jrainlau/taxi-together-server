import json

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
			'name': ctxBody['name'],
			'avatar': ctxBody['avatar']
		}
		bill = {
			'billId': ctxBody['billId'],
			'members': [user]
		}
		if ctxBody['userId'] in [item['userId'] for item in self.inBillUsers]:
			return response('用户已存在于拼单中！', 1)
		self.billsList.append(bill)
		self.inBillUsers.append(user)
		return response({
			'billsList': self.billsList,
			'inBillUsers': self.inBillUsers
		})

	def enterBill(self, ctx):
		ctxBody = ctx.form
		billId = ctxBody['billId']
		user = {
			'userId': ctxBody['userId'],
			'name': ctxBody['name'],
			'avatar': ctxBody['avatar']
		}
		if ctxBody['userId'] in [item['userId'] for item in self.inBillUsers]:
			return response('用户已存在于拼单中！', 1)
		theBill = [item for item in self.billsList if item['billId'] == billId]
		if not theBill:
			return response('拼单不存在', 1)
		theBill[0]['members'].append(user)
		self.inBillUsers.append(user)
		return response({
			'billsList': self.billsList,
			'inBillUsers': self.inBillUsers
		})

	def leaveBill(self, ctx):
		ctxBody = ctx.form
		billId = ctxBody['billId']
		user = {
			'userId': ctxBody['userId']
		}
		try:
			userIndex = [self.inBillUsers.index(item) for item in self.inBillUsers if item['userId'] == user['userId']][0]
			memberIndex = [self.billsList.index(item) for item in self.billsList if item['billId'] == billId][0]
			del self.inBillUsers[userIndex]
			del [item['members'] for item in self.billsList if item['billId'] == billId][0][memberIndex]
			return response({
				'billsList': self.billsList,
				'inBillUsers': self.inBillUsers
			})
		except IndexError:
			return response('无法重复退出拼单！', 1)

	def getBill(self, ctx):
		ctxBody = ctx.form
		billId = ctxBody['billId']
		return response([item for item in self.billsList if item['billId'] == billId])

	def completeBill(self, ctx):
		ctxBody = ctx.form
		billId = ctxBody['billId']
		theBill = [item for item in self.billsList if item['billId'] == billId]
		if not theBill:
			return response('拼单不存在', 1)
		memberIds = [item['userId'] for item in theBill[0]['members']]
		for memberId in memberIds:
			try:
				userIndex = [self.inBillUsers.index(item) for item in self.inBillUsers if item['userId'] == memberId][0]
				del self.inBillUsers[userIndex]
			except:
				return response('用户不存在', 1)
		try:
			billIndex = [self.billsList.index(item) for item in self.billsList if item['billId'] == billId][0]
			del self.billsList[billIndex]
		except:
			return response('账单不存在', 1)
		return response({
			'billsList': self.billsList,
			'inBillUsers': self.inBillUsers
		})
		