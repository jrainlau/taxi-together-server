const response = require('../utils/index.js')

const billsList = []
const inBillUsers = []

class BillController {
  createBill (ctx) {
    const requestBody = ctx.request.body
    const user = {
      userId: requestBody.userId,
      name: requestBody.name,
      avatar: requestBody.avatar
    }
    const bill = {
      billId: requestBody.billId,
      members: [user]
    }
    if (inBillUsers.map(({ userId }) => userId).includes(requestBody.userId)) {
      ctx.body = response('用户已存在于拼单中！', 1)
      return
    }
    billsList.push(bill)
    inBillUsers.push(user)
    ctx.body = response({
      billsList,
      inBillUsers
    })
  }

  enterBill (ctx) {
    const requestBody = ctx.request.body
    const billId = requestBody.billId
    const user = {
      userId: requestBody.userId,
      name: requestBody.name,
      avatar: requestBody.avatar
    }
    if (inBillUsers.map(({ userId }) => userId).includes(requestBody.userId)) {
      ctx.body = response('用户已存在于拼单中！', 1)
      return
    }
    const theBill = billsList.find(bill => bill.billId === billId)
    if (!theBill) {
      ctx.body = response('拼单不存在', 1)
      return
    }
    theBill.members.push(user)
    inBillUsers.push(user)
    ctx.body = response({
      billsList,
      inBillUsers
    })
  }

  leaveBill (ctx) {
    const requestBody = ctx.request.body
    const billId = requestBody.billId
    const user = {
      userId: requestBody.userId,
      name: requestBody.name,
      avatar: requestBody.avatar
    }
    const userIndex = inBillUsers.findIndex(({ userId }) => userId === user.userId)
    const memberIndex = billsList.findIndex(bill => bill.billId === billId)
    inBillUsers.splice(userIndex, 1)
    billsList.filter(bill => bill.billId === billId)[0].members.splice(memberIndex, 1)
    ctx.body = response({
      billsList,
      inBillUsers
    })
  }

  getBill (ctx) {
    const requestBody = ctx.request.body
    const billId = requestBody.billId
    ctx.body = response(billsList.filter(bill => bill.billId === billId))
  }

  completeBill (ctx) {
    const requestBody = ctx.request.body
    const billId = requestBody.billId
    const theBill = billsList.find(bill => bill.billId === billId)
    if (!theBill) {
      ctx.body = response('拼单不存在', 1)
      return
    }
    const memberIds = theBill.members.map(({ userId }) => userId)
    memberIds.forEach((id) => {
      const userIndex = inBillUsers.findIndex(({ userId }) => userId === id)
      inBillUsers.splice(userIndex, 1)
    })
    const billIndex = billsList.findIndex(bill => bill.billId === billId)
    billsList.splice(billIndex, 1)
    ctx.body = response({
      billsList: billsList,
      inBillUsers: inBillUsers
    })
  }
}

module.exports = new BillController()
