This is a project that uses KSL, (it's like craiglist) and adds notification support. It does it through email. KSL has an undocumented api, but I've found it to be a little unreliable. The cool thing about this project is that it does most of the loading through selenium and then parses from there.

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

# DEPENDENCIES
BeautifulSoup

SELENIUM

SELENIUM CHROM DRIVER

JSON

SMTPLIB

email.mime.multipart

email.mime.text

pprint
