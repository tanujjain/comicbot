# comicbot
Facebook chatbot for reading my favourite comics. It gives the current day's comicstrip.
The following comics have been used:
* [Daily Dilbert](http://dilbert.com/)
* [xkcd](https://xkcd.com/)
* [Calvin & Hobbes](https://www.gocomics.com/calvinandhobbes/)

#  Architecture

A python web application was developed using [Flask](http://flask.pocoo.org/).
Following components are involved in the bot:
* Scraper: Written in python, uses packages: requests, BeautifulSoup
* [Heroku](https://www.heroku.com/): For hosting
* [Facebook messenger chatbot API](https://developers.facebook.com/docs/messenger-platform/reference/send-api/)

### Interconnections

The web application is written using python microserver framework [Flask](http://flask.pocoo.org/) and was hosted on Heroku.

The web address of the app(given by Heroku), is then used as a webhook that the facebook messenger uses to invoke the hosted app logic. When the user types in a specific keyword to get a particular comic, eg: 'dilbert' for Daily Dilbert comic, the webhook to this web app is triggered and the text 'dilbert' is sent to the webapp logic. The keyword 'dilbert' invokes a function that scrapes the related website to get the current day's comic strip and sends the response back to the facebook chatbot. The response is a URL to the comic which gets rendered by the bot itself (some facebook logic, hidden from us developers).

There are specific keywords for each comic strip:
* 'dilbert' for Daily Dilbert
* 'xkcd' for xkcd comics
* 'cal' for Calvin & Calvin & Hobbes
* 'all' for all the 3 comics

# Development Strategy

The app was developed in several iterations as described below:

### Iteration 0:

_Expected output_: The chatbot is capable of echoing the text messages sent to it. This logic should work locally and the app should not be hosted publically at this point.

This iteration was done to understand the interaction between facebook messenger api and the flask app.

To connect the web application to the flask app logic, a webhook is required as mentioned previously. This presented a problem since at this point, the app was still not hosted on the web. Luckily, there are tools such as [ngrok](https://ngrok.com/) which can bind one of the local webports with a public IP. The installation of ngrok on mac is as simple as it can get: `brew cask install ngrok` . The flask app was assigned a local port address such as: `127.0.0.1:5000`. This means that the app, when run locally, will throw its traffic at port 5000 of the localhost address. Using the command: `ngrok http 5000`in the terminal gave a public IP which could be then used to provide a public IP to the local port and thus, can be used as a webhook to be configured into the facebook messenger.

No scraping logic was deployed upto this point.

### Iteration 1:


_Expected output_: The chatbot is capable of sending one scraped comic when a particular text string is given by a user to the bot. This logic should work locally and the app should not be hosted publically at this point.

This iteration builds upon the last one and helps understand the facebook messenger api for sending URLs to the bot. The scraping logic for Daily Dilbert was deployed and tested to see if the bot can receive the url and render the images to be displayed. The app is still running locally and hooked to the fb messenger using ngrok as described previously.

### Iteration 2:


_Expected output_: The chatbot is capable of sending one scraped comic when a particular text string is given by a user to the bot and that the application is now hosted onto Heroku.

This iteration helped understanding how applications can be deployed on Heroku, how Heroku can be hooked up with a  github repo (instead of the default heroku one) and how different branches of the repo can be deployed instead of the master. Additionally, it helped understand credential management through heroku so that access tokens and other sensitive information is can be populated at runtime without the need to hard-code it onto a public github repo.

The conclusion of this iteration resulted in a **minimum viable product(MVP): A chatbot capable of output-ing a single scraped comic.**


### Iteration 3:


_Expected output_: The chatbot is capable of sending all the scraped comics when the respective particular text string is given by a user to the bot and that the application is now hosted onto Heroku.

This iteration extended the last one by addition of the scraping logic for other comics to the existing code. This would allow the end user to input specific text to get specific comics. Additionally, a single command could be used to get all the 3 comic strips for the day.
