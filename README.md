This is a project that uses KSL, (it's like craiglist) and adds notification support. It does it through email. KSL has an undocumented api, but I've found it to be a little unreliable. The cool thing about this project is that it does most of the loading through selenium and then parses from there. Just so we're very clear with each other. This is not intended for an in-depth example of how to get notifications from KSL. Rather it was a "I need a new car, what's something I could write in less than a day to help with that" project.

# HOW TO USE
Depending on whether you would like to querey items or cars use the getCarInfo or the GetItems files.

In either case fill in the following info in the file you wish to use

```python
yourEmail = "EMAIL YOU WISH TO EMAIL"
emailUserName = "YOUR USERNAME"
emailPassword = "YOUR EMAIL PASSWORD"
```


Then  fill in the link getting the url after you've searched the results you're interested in. 
	More explanaition:
		Go to either https://classifieds.ksl.com/ or https://www.ksl.com/auto/ depending on if you're buying a car or an item
		Once you've filled in your desired search configuration hit search
		Grab url from page after search has completely loaded.
		This is the url you fill in the links section.

`links = "https://classifieds.ksl.com/search/?keyword=pixel&zip=&miles=25&priceFrom=%2480&priceTo=%24350&marketType%5B%5D=Sale&city=&state=&sort=0"`

That's it.

# Installation

1. FILL OUT THE INFO DESCRIBED IN HOW TO USE
2. Download the chrome driver using the link under dependencies. (You may need chrome installed as well)
3. Add the chrome driver to your path or paste it in the project directory. If using docker paste it in the project directory.
4. Follow the steps below

USING DOCKER
`docker-compose up`
RUN (crontab -l ; echo "* * * * * echo "Hello world" >> /var/log/cron.log") | crontab

NOT USING DOCKER
`pip install -r requirements.txt`
Now you need to set up a cron job (or windows scheduler) to run the python scripts.

By default the cron scripts were already written. All you should have to do is uncomment the desired feature, be it the search of the KSL Cars or the KSL Items.
If you want the


# DEPENDENCIES
BeautifulSoup

SELENIUM

SELENIUM CHROME DRIVER -- http://chromedriver.chromium.org/downloads

pprint
