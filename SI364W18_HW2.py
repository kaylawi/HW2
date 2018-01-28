## SI 364
## Winter 2018
## HW 2 - Part 1

## Collboarated with Chalse Okorom and Amanda Gomez 
## This homework has 3 parts, all of which should be completed inside this file.

## Add view functions and any other necessary code to this 
## Flask application code below so that the routes described
## in the README exist and render the templates they are 
## supposed to (all templates provided are inside the 
## templates/ directory, where they should stay).

## As part of the homework, you may also need
## to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################

from flask import Flask, request, render_template, url_for, flash,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json 

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################

##Add a form to the application in `SI364W18_HW2.py`,
##using `WTForms` syntax. The class name should be `AlbumEntryForm`.**

##The `AlbumEntryForm` should have the following fields:

##Text entry for an album name, whose label should be
## `Enter the name of an album:`, which should be **required**
##Radio buttons with options: 1,2,3 -- representing 
##how much the user likes the album, whose label should be: 
##`How much do you like this album? (1 low, 3 high)`,
## which should be **required**
## A submit button

##Then, add 2 more routes to the application:**

##`/album_entry`, which should render the WTForm 
##you just created (note that there is a raw HTML form in one
## of the provided templates, but THIS should rely on your WTForms form). It should send data to a template called `album_entry.html` (see Part 3). The form should look pretty much [like this](https://www.dropbox.com/s/6mvt6d4b929vu0n/Screenshot%202018-01-15%2016.10.09.png?dl=0) **when you are done with Part 3.**

## `/album_result`, which should render the results of what
## was submitted to the `AlbumEntryForm`,
## [like this](https://www.dropbox.com/s/vqi7ybmkdh7ca1q/
##Screenshot%202018-01-15%2016.07.38.png?dl=0) 
##when you are done with Part 3.** It should send data 
##to a template called `album_data.html` (see Part 3).

class AlbumEntryForm(FlaskForm):

	album =StringField("Enter the name of an album:", validators=[Required()])
	rating=RadioField('How much do you like this album?', validators=[Required()], choices = [('1',1),('2',2),('3',3)]) #option,value
	submit =SubmitField('Submit')

@app.route('/album_entry', methods = ['GET','POST'])
def entry():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		album = form.album.data
		rating = form.rating.data
		simpleForm = AlbumEntryForm()
	return render_template('album_entry.html', form=form)

@app.route('/album_result', methods = ['GET','POST'])
def result(): 
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		a = form.album.data
		r = form.rating.data
		simpleForm = AlbumEntryForm()
		return render_template('album_data.html', album=a, rating=r) #these parameters being passed into an object 
	flash('All fields are required!')
	return redirect(url_for('entry'))

####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)

@app.route('/artistform')
def form():
	return render_template("artistform.html")

@app.route('/artistinfo', methods = ['GET']) #Only use get method if you are sending information to the form 
def info():
	if request.method == 'GET':
		result = request.args['artist'] #going inside of the dictionary to get the artist info(string) #get artist from the form #only need this line when you are using a request method 
		url = requests.get('https://itunes.apple.com/search?term={}&country=US&entity=musicTrack'.format(result)) #term is searching through itunes api
		#entity searches through media
		#can have more than one parameter 
		data = url.json()['results'] #reads the information from the url and reads it 
		#requests come in two dictionaries, one is a number of results and other one is a list of results
		return render_template('artist_info.html',objects = data)

@app.route('/artistlinks')
def links():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist>') #Dont need a method because it will just display the results 
def specific(artist):

	url = requests.get('https://itunes.apple.com/search?term={}&country=US&entity=musicTrack'.format(artist)) #only requesting from itunes api #pass in artist 
	data = url.json()['results']
	return render_template('specific_artist.html',results = data)


if __name__ == '__main__':
    app.run(use_reloader=True,debug=True)
