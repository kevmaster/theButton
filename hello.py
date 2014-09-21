from flask import Flask
from flask import request
import time
import json
#runs at startup, sets up the server and variables
def create_app():
	app = Flask(__name__)
	app.g = [0,0,0,[],{}]
	def gethighscore():
		highscore = open('highscore','r')
		highscore = highscore.read()
		app.g[2] = highscore
	def setupdb():
		db = open('ips','r')
		db = json.load(db)
		app.g[3] = db
	gethighscore()
	setupdb()
	return app

#app.g[0] is number of buttons currently pushed
#app.g[1] is timer variable (last time button wasn't pushed)
#app.g[2] is current high score
#app.g[3] is database of IPs and number of button presses
#app.g[4] is a map of IPs and last pressed times

app = create_app()

#saves high score to a file
def savehighscore():
	highscore = open('highscore','w')
	highscore.write(str(app.g[2]))
	highscore.close()
	return

def addlastpress(ip):
	app.g[4][ip]=time.time()
	return

def removelastpress(ip):
	del app.g[4][ip]
	return

def savedb():
	db = open('ips','w')
	json.dump(app.g[3],db)
	db.close()
	return

def addpush(ip):
	addlastpress(ip)
	for x in app.g[3]:
		if x[0] == ip:
			x[1] = x[1]+1
			savedb()
			return
	app.g[3].append([ip,1,0,0])
	savedb()
	return

def addrelease(ip):
	for x in app.g[3]:
		if x[0] == ip:
			x[2] = x[2]+1
			diff = int(time.time() - app.g[4][ip])
			removelastpress(ip)
			if diff>x[3]:
				x[3] = diff
			savedb()
			return
	app.g[3].append([ip,1,0,0])
	savedb()
	return

@app.route("/personal", methods=['GET'])
def personal():
	for x in app.g[3]:
		if x[0] == request.remote_addr:
			return str(x[3])
	return '0'

#returns the current timer time
@app.route("/timer", methods=['GET'])
def timer():
	if app.g[0] == 0:
		app.g[1] = time.time()
	return str(int(time.time() - app.g[1]))

#adds one to the buttons pushed variable
@app.route("/push", methods = ['POST'])
def push():
	addpush(request.remote_addr)
	print 'pushing button'
	if app.g[0]==0:
		app.g[1] = time.time()
	app.g[0] = app.g[0] + 1
	return timer()

#removes one from the buttons pushed variable, resets timer if its the last button,
#and sets high score if higher than last one
@app.route("/release", methods = ['POST'])
def release():
	addrelease(request.remote_addr)
	number = int(time.time()-app.g[1])
	print 'releasing button with current score: '+str(number)+' and old highscore: '+str(app.g[2])
	app.g[0] = app.g[0] - 1
	if app.g[0]==0:
		if int(number)-int(app.g[2])>=0:
			print 'current score is higher than highscore'
			app.g[2]=number
			savehighscore()
		app.g[1] = time.time()
	return str(app.g[0])

#returns number of pushed buttons
@app.route("/stack", methods = ['POST'])
def stack():
	return str(app.g[0])

#returns current highscore
@app.route("/highscore", methods = ['GET'])
def highscore():
	return str(app.g[2])

if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0', debug= True)
