const Router = require('koa-router')
const BillController = require('../controller/bill.js')

const bill = new Router()

bill
  .post('/create', BillController.createBill)
  .post('/enter', BillController.enterBill)
  .post('/leave', BillController.leaveBill)
  .post('/get', BillController.getBill)
  .post('/complete', BillController.completeBill)

module.exports = bill
