This is a project that uses KSL, (it's like craiglist) and adds notification support. It does it through email. KSL has an undocumented api, but I've found it to be a little unreliable. The cool thing about this project is that it does most of the loading through selenium and then parses from there. Just so we're very clear with each other. This is not intended for an in-depth example of how to get notifications from KSL. Rather it was a "I need a new car, what's something I could write in less than a day to help with that" project.

# HOW TO USE

## USING DOCKER

`docker-compose up`

## USING PYTHON
`python3 src/KSL-Items/getItemList.py`
`python3 src/KSL-Items/getCar.py`

OR

`python src/KSL-Items/getItemList.py`
`python src/KSL-Items/getCar.py`

# INSTALLATION

Depending on whether you would like to querey items or cars use the getCarInfo or the GetItems files.

In either case fill in the following info in the file you wish to use

```python
yourEmail = "EMAIL YOU WISH TO EMAIL"
emailUserName = "YOUR USERNAME"
emailPassword = "YOUR EMAIL PASSWORD"
```

## Getting the link to search

Then  fill in the link getting the url after you've searched the results you're interested in. 
	More explanaition:
		Go to either https://classifieds.ksl.com/ or https://www.ksl.com/auto/ depending on if you're buying a car or an item
		Once you've filled in your desired search configuration hit search
		Grab url from page after search has completely loaded.
		This is the url you fill in the links section.

`links = "https://classifieds.ksl.com/search/?keyword=pixel&zip=&miles=25&priceFrom=%2480&priceTo=%24350&marketType%5B%5D=Sale&city=&state=&sort=0"`

## Setting up email

To get the email username and emailpassword listed above you need to get access to your gmail account. Here are the gmail links below on how to do that
https://support.google.com/accounts/answer/185833?hl=en
https://myaccount.google.com/apppasswords

## Running in commandline (no docker)
`pip install -r requirements.txt`

OR

`pip3 install -r  requirements.txt`

### Setting up Chromedriver
**SKIP THIS IF USING DOCKER**

If running locally and not in the docker you need to have google chrome installed. You then need to go download your google chrome driver that matches your google chrome version.
http://chromedriver.chromium.org/downloads

After you've downloaded it you need to include it in your PATH enviroment variable. How you will do this will depend on which OS you're running.


## Docker and Cron setup

To have it run regularaly using the cronjob you have to edit some more things.

you'll need to go into the `DOCKERFILE` and change the `ENV TZ=America/Denver` line to reflect the timezone that you want it to represent. 

You'll aslo have to the `crontab` file and uncomment/comment out the one you want to use. It defaults to the KSL Classifieds for items. If desired you can also change the intervals. Right now it runs every minute from 8-10:59.




# DEPENDENCIES
Google Chrome

BeautifulSoup

SELENIUM

SELENIUM CHROME DRIVER -- http://chromedriver.chromium.org/downloads

pprint

# Known issues
Chromium and the chrome driver can get out of sync. I still need to figure out how to load it in dynamically based on version.
