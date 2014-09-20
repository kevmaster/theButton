from flask import Flask
import time
app = Flask(__name__)

#def main():
stack = 0
#app.g = 0

@app.route("/timer", methods=['GET'])
def timer():
	if stack == 0:
		app.g = time.time()
	return str(int(time.time() - app.g))

@app.route("/push", methods = ['POST'])
def push():
	if stack==0:
		app.g = time.time()
	stack = stack + 1
	return timer()

@app.route("/release", methods = ['POST'])
def release():
	stack = stack - 1
	if stack==0:
		app.g = time.time()
	return str(stack)

if __name__ == "__main__":
	app.g = 0
	app.debug = True
	app.run(host = '0.0.0.0', debug= True)
