from flask import Flask, request
from controller import bill

controller = bill.BillController()
app = Flask(__name__)

@app.route('/create', methods = ['POST'])
def create():
	return controller.createBill(request)

@app.route('/enter', methods = ['POST'])
def enter():
	return controller.enterBill(request)

@app.route('/leave', methods = ['POST'])
def leave():
	return controller.leaveBill(request)

@app.route('/get', methods = ['POST'])
def get():
	return controller.getBill(request)

@app.route('/complete', methods = ['POST'])
def complete():
	return controller.completeBill(request)

if __name__ == '__main__':
    app.run()
