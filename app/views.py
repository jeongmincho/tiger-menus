import urllib2
from bs4 import BeautifulSoup
from flask import render_template
import datetime
from app import app

roma    = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=01'
wucox   = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=02'
forbes  = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=03'
grad    = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=04'
cjl     = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=05'
whitman = 'https://campusdining.princeton.edu/dining/_Foodpro/menuSamp.asp?locationNum=08'

#database
halls = [wucox, cjl, whitman, roma, forbes, grad]
lunchList = [[] for x in range(6)]
dinnerList = [[] for x in range(6)]
lastDate = datetime.datetime.today().weekday()

#update database
def scrape():
	global lunchList
	global dinnerList
	lunchList = [[] for x in range(6)]
	dinnerList = [[] for x in range(6)]
	lunch = False
	dinner = False

	for i in range(6):
		response = urllib2.urlopen(halls[i])
		html = response.read()
		soup = BeautifulSoup(html, 'html.parser')

		for string in soup.stripped_strings:
			if string == 'Lunch':
				lunch  = True
			if string == 'Dinner':
				lunch  = False
				dinner = True
			if string == 'Powered by FoodPro':
				dinner = False
			if lunch:
				lunchList[i].append(string)
			if dinner:
				dinnerList[i].append(string)

#scrape when server starts
scrape()

#check if menus have changed
def checkForUpdate():
	global lastDate
	currentDay = datetime.datetime.today().weekday()
	if currentDay != lastDate:
		scrape()
		lastDate = currentDay


@app.route('/lunch')
def lunch():
	checkForUpdate()

	return render_template( "meal.html",
							wucox = lunchList[0],
							cjl = lunchList[1],
							whitman = lunchList[2],
							roma = lunchList[3],
							forbes = lunchList[4],
							grad = lunchList[5])


@app.route('/dinner')
def dinner():
	checkForUpdate()

	return render_template(	"meal.html",
							wucox = dinnerList[0],
							cjl = dinnerList[1],
							whitman = dinnerList[2],
							roma = dinnerList[3],
							forbes = dinnerList[4],
							grad = dinnerList[5])

#homepage will default
@app.route('/')
def index():
	now = datetime.datetime.now()
	if now.hour < 14:
		return lunch()
	else:
		return dinner()


