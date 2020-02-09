from flask import Flask, request, render_template, session, redirect, url_for
import os
import operator
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
#set up database
project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "races.db"))

app = Flask(__name__)
app.secret_key = "abc"

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Race (db.Model):
    uid = db.Column (db.Integer, primary_key = True)
    p1=db.Column(db.Text())
    p2=db.Column(db.Text())
    w=db.Column(db.Text())
    def __init__(self, p1, p2, w):
        self.p1=p1
        self.p2=p2
        self.w = w

@app.route ("/adminlogin/")
def adminlogin():
	if 'login' in session and session['login'] == 'true' :
		return render_template ('addrace.html')
	return render_template ('adminlogin.html')

@app.route ("/verifylogin/", methods = ['POST'])
def verifylogin ():
	uname = request.form['username']
	pword = request.form['password']
	if pword == "password":
		session['login']='true'
		return redirect (url_for ('add'))
	else:
		print ('here')
		return redirect (url_for('adminlogin'))

@app.route ("/logout/")
def logout ():
	session.pop ('login', None)
	return 'user logged out'



@app.route ('/add/')
def add ():
	if 'login' in session and session['login'] == 'true' :
		return render_template ('addrace.html')
	else:
		return 'please login'

@app.route('/adminportal/', methods = ['POST'])
def adminportal():
	if 'login' in session and session['login'] == 'true' :
		p1 = request.form['p1']
		p2 = request.form ['p2']
		w = request.form ['w']
		db.session.add (Race(p1, p2, w))
		db.session.commit()
		print (Race.query.first())
		return 'ok'
	else:
		return 'not logged in'

@app.route ('/viewraces/')
def viewraces():
	races = Race.query.all()
	return render_template ("viewraces.html", races=races)

@app.route ("/currentstandings/")
def currentstandings():
	races = Race.query.all()
	dict={}
	for r in races:
		if r.w not in dict:
			dict[r.w]=1
		else:
			dict[r.w]=dict[r.w]+1
	#sort based on no of games won descending		
	sorted_d = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)
	print (sorted_d)
	return render_template ("currentstandings.html", dict = dict)

if __name__ == '__main__':
	db.create_all()
	app.run ()