# im_futuretest_flask
These are the flask utilities for the im_futuretest library. If your project uses flask, this is the package you want.

## Install 

Use the python package for this library. You can find the package online [here](https://pypi.org/project/im-futuretest/).

Change to your Python App Engine project's root folder and do the following:

> pip install appenginetaskutils --target lib

Or add it to your requirements.txt. You'll also need to set up vendoring, see [app engine vendoring instructions here](https://cloud.google.com/appengine/docs/python/tools/using-libraries-python-27).

## Configuring im_futuretest_flask

This package provides functions that register flask handler functions for im_futuretest_flask, both for its api and its ui.

To get your tests running properly, you should register these handlers in your main app (wherever your main flask app is constructed). Doing this 
ensures that your tests have exactly the same code loaded as the code they're testing would have when being used normally, ie: no dependency hell.

### app.yaml

The futuretest handlers all have routes of the form:
/futuretest/XXX
(where XXX may include more levels of pathing)

Say you already have an app.yaml rule which pushes all routes to your main app, say main.py, as follows:

	handlers:
		- url: *
		  script: main.app

Then this will work for futuretest without any modification.

If things are a little messy, you can just add this somewhere early in app.yaml:

	- url: /futuretest/*
	  script: main.app
	  login: admin

This will direct all futuretest routes to the "app" flask application constructed in main.py. Obviously modify this as needed.

Also note the requirement for the user to be an admin of your project. Futuretest is designed to run potentially long running and expensive 
tests; it's best not to open that up to all comers!

### main.py

Now traffic is going to the app constructed in main.py.

Next we need to register the futuretest flask handlers with your app.

Do it like this:

	from flask import Flask
	from flaskhandlers import register_tests_api
	... other imports ...

	app = Flask(__name__)  # creating your app

	... add other handlers to your app, etc ...

	register_futuretest_handlers(app) # this adds IM Future Test's handlers

	... do more stuff with app ...

ie: just call register_futuretest_handlers(app) somewhere in main.py

### Accessing the UI

Go to the url

	http(s)://<yourdomain>/futuretest/ui

and you'll see the UI:

![IM Future Test screenshot](https://lh6.googleusercontent.com/Q5XUfYdQ6ZkJSjSFdcDz5AQieAv7c-f_pwrVBtFuv0p_UC46yBh5ijC1SL8qu1pgsyzJPf-hFrGV2w=w1615-h935 "IM Future Test screenshot")





