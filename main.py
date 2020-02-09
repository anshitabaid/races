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


#model for Race database entry
class Race (db.Model):
    uid = db.Column (db.Integer, primary_key = True)
    p1=db.Column(db.Text())
    p2=db.Column(db.Text())
    w=db.Column(db.Text())
    def __init__(self, p1, p2, w):
        self.p1=p1
        self.p2=p2
        self.w = w

#for admin login
@app.route ("/login/")
def login():
	if 'login' in session and session['login'] == 'true' :
		return render_template ('addrace.html', msg = "Admin already logged in")
	return render_template ('adminlogin.html')

#to verify login credentials. As of now, username = username and password = password to login
@app.route ("/verifylogin/", methods = ['POST'])
def verifylogin ():
	uname = request.form['username']
	pword = request.form['password']
	if pword == "password" and uname=="username":
		session['login']='true'
		return redirect (url_for ('add'))
	else:
		print ('here')
		return render_template ("adminlogin.html", msg="Incorrect values, please try again")

#admin logout
@app.route ("/logout/")
def logout ():
	session.pop ('login', None)
	return render_template ("adminlogin.html", msg = "User logged out")

#admin can add race details here
@app.route ('/add/')
def add ():
	#check if admin is already logged in
	if 'login' in session and session['login'] == 'true' :
		return render_template ('addrace.html')
	else:
		return render_template ("adminlogin.html", msg = "Please login as admin")

#if logged, in, this route extracts the fields from form and submits to db
#TODO: sanitize and validate data
@app.route('/adminportal/', methods = ['POST'])
def adminportal():
	if 'login' in session and session['login'] == 'true' :
		p1 = request.form['p1']
		p2 = request.form ['p2']
		w = request.form ['w']
		if (p1==w) or (p2==w):
			db.session.add (Race(p1, p2, w))
			db.session.commit()
			return render_template ("index.html", msg = "Race added")
		else:
			return render_template ("addrace.html", msg="Incorrect values, try again")
	else:
		return 'not logged in'

#for everyone to view races, players, winners
@app.route ('/viewraces/')
def viewraces():
	races = Race.query.all()
	return render_template ("viewraces.html", races=races)

#view current standings in asc/desc order as specified in argument in url
@app.route ("/currentstandings")
def currentstandings():
	order = request.args['sort']
	races = Race.query.all() #details of all races
	#create a dict to calculate who won how many races
	dict={}
	for r in races:
		if r.w not in dict:
			dict[r.w]=1
		else:
			dict[r.w]=dict[r.w]+1
	#sort based on no of games won descending, the no of games won will be value in key-value pair in dict
	if (order == None) or (order == 'desc'):
		sorted_d = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}
		return render_template ("currentstandings.html", dict = sorted_d)
	else:
		sorted_d = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
		return render_template ("currentstandings.html", dict = sorted_d)

#index
@app.route ('/')
def home():
	return render_template ("index.html")

if __name__ == '__main__':
	db.create_all()
	app.run ()