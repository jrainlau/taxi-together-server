from flask import Flask, request, send_from_directory
from controller import bill

controller = bill.BillController()
app = Flask(__name__)

@app.route('/create', methods = ['POST'])
def create():
	return controller.createBill(request)

@app.route('/join', methods = ['POST'])
def join():
	return controller.joinBill(request)

@app.route('/leave', methods = ['POST'])
def leave():
	return controller.leaveBill(request)

@app.route('/getBill', methods = ['POST'])
def getBill():
	return controller.getBill(request)

@app.route('/inBill', methods = ['POST'])
def inBill():
	return controller.inBill(request)

@app.route('/uploadImg', methods = ['POST'])
def uploadImg():
	return controller.uploadImg(request)

@app.route('/getImg/<filename>')
def getImg(filename):
  return send_from_directory('./imgs', filename)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
