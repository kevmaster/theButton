from flask import Flask
import time
app = Flask(__name__)

#def main():
stack = []
#app.g = 0

@app.route("/timer", methods=['GET'])
def timer():
	if len(stack) == 0:
		app.g = time.time()
	return str(int(time.time() - app.g))

@app.route("/push", methods = ['POST'])
def push():
	if len(stack)==0:
		app.g = time.time()
	stack.append('x')
	return str([timer(),len(stack)])

@app.route("/release", methods = ['POST'])
def release():
	stack.pop()
	if len(stack)==0:
		app.g = time.time()
	return str([timer(),len(stack)])

if __name__ == "__main__":
	app.g = 0
	app.debug = True
	app.run(host = '0.0.0.0', debug= True)
