from flask import Flask
import time
app = Flask(__name__)

#def main():
#app.g = 0

@app.route("/timer", methods=['GET'])
def timer():
	if app.g[0] == 0:
		app.g[1] = time.time()
	return str(int(time.time() - app.g[1]))

@app.route("/push", methods = ['POST'])
def push():
	if app.g[0]==0:
		app.g[1] = time.time()
	app.g[0] = app.g[0] + 1
	return timer()

@app.route("/release", methods = ['POST'])
def release():
	app.g[0] = app.g[0] - 1
	if app.g[0]==0:
		app.g[1] = time.time()
	return str(app.g[0])

@app.route("/stack", methods = ['POST'])
def stack():
	return str(app.g[0])

if __name__ == "__main__":
	app.g = [0,0]
	app.debug = True
	app.run(host = '0.0.0.0', debug= True)
