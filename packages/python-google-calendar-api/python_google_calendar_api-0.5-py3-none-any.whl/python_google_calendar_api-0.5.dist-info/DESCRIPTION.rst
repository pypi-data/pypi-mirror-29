==========================
Python Google calendar api
==========================

This package demonstrates a simple implementation of Google calendar api and let you create and update events.

Description
-----------

1. The first step is to turn on your google calendar api.

   a. Use the following link to create or select a project from the google developer console and turn on the api.

      https://console.developers.google.com/start/api?id=calendar

      Click continue and go to credentials.

   b. On the Add credentials to your project page, click the Cancel button.

   c. At the top of the page, select the OAuth consent screen tab. Select an Email address, enter a Product name if not already set, and click the Save button.

   d. Select the Credentials tab, click the Create credentials button and select OAuth client ID.

   e. Select the application type "Other", enter the desired name, and click the Create button.

   f. Click OK to dismiss the resulting dialog.

   g. Click the Download JSON button to the right of the client ID.

   h. Move this file to your projects home directory and rename it client_secret.json.

2. Install the package using the folowing command

    pip install python-google-calendar-api

3. Once the client_secret.json file is in your projects home directory and the this package is installed, you are able to create and update events on your google calendar.

4. Example code:

from calendar_api.calendar_api import google_calendar_api
m=google_calendar_api()
m.create_event(calendar_id='<your calendar id>',
	start='2017,12,5,15,00,00',
	end='2017,12,5,15,15,00'
	description='foo'
	)


