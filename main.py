from config import *
from models import *
from globals import *
from helpers import *


#for admin login
@app.route ("/login/")
def login():
	if isLoggedIn():
		return render_template ('addrace.html', msg = "Admin already logged in")
	return render_template ('adminlogin.html')

#to verify login credentials. As of now, username = username and password = password to login
@app.route ("/verifylogin/", methods = ['POST'])
def verifylogin ():
	#hash input passwords and verify 
	uname = request.form['username'].split()[0]
	pword = request.form['password'].split()[0]
	h = hashlib.md5 (pword.encode("utf8")).hexdigest()
	if uname=="username" and h==ADMIN_PW_HASH:
		session[LOGIN]=TRUE
		return redirect (url_for ('add'))
	else:
		return render_template ("adminlogin.html", msg="Incorrect values, please try again")

#admin logout
@app.route ("/logout/")
def logout ():
	session.pop (LOGIN, None)
	return render_template ("index.html", msg = "User logged out")

#admin can add race details here
@app.route ('/add/')
def add ():
	#check if admin is already logged in
	if isLoggedIn():
		return render_template ('addrace.html')
	else:
		return render_template ("adminlogin.html", msg = "Please login as admin")

#if logged, in, this route extracts the fields from form and submits to db
@app.route('/adminportal/', methods = ['POST'])
def adminportal():
	if isLoggedIn():
		p1 = request.form['p1']
		p2 = request.form ['p2']
		w = request.form ['w']
		#remove trailing whitespaces
		p1 = p1.split ()[0]
		p2 = p2.split ()[0]
		w = w.split ()[0]
		#check for valid data
		if validateData (p1, p2, w)==True:
			db.session.add (Race(p1, p2, w))
			db.session.commit()
			insertPlayer(p1)
			insertPlayer(p2)
			updateWinCount (w)
			return render_template ("index.html", msg = "Race added")
		else:
			return render_template ("addrace.html", msg="Incorrect values, try again")
	else:
		return render_template ("adminlogin.html", msg = "Please login as admin")

#for everyone to view races, players, winners
@app.route ('/viewraces/')
def viewraces():
	name_filter = request.args ['player']
	if name_filter == '':
		races = Race.query.all()
	else:
		races = Race.query.filter((Race.p1==name_filter) | (Race.p2==name_filter ))
	return render_template ("viewraces.html", races=races)

#view current standings 
@app.route ("/currentstandings/")
def currentstandings():
	order = request.args['AscOrDesc']
	name_filter = request.args ['player']
	if name_filter == "":
		players = Player.query.all() #details of all players
	else:
		players = Player.query.filter_by(name=name_filter) #details of only required players
	#create a dict to calculate who won how many races
	dict={}
	for p in players:
		dict[p.name]=p.wins
	#sort based on no of games won descending, the no of games won will be value in key-value pair in dict
	if (order == None) or (order == 'desc'):
		sorted_d = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse=True)}
		return render_template ("currentstandings.html", dict = sorted_d)
	else: #sort based on ascending
		sorted_d = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}
		return render_template ("currentstandings.html", dict = sorted_d)

"""
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
"""

#index, runs on localhost:5000
@app.route ('/')
def home():
	return render_template ("index.html")

if __name__ == '__main__':
	db.create_all()
	app.run ()
