from bs4 import BeautifulSoup
import os, sys
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import http.client, urllib	

### Global Functions
def str_to_bool(s):
	t = s.lower()
	if t == 'true':
		 return True
	elif t == 'false':
		 return False
	else:
		 raise ValueError # evil ValueError that doesn't tell you what the wrong value was

### Other Config
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = ROOT_DIR + "/itemsList.txt"
load_dotenv(dotenv_path=ROOT_DIR + "/../../.env")

### FEATURES
usePushover = str_to_bool(os.getenv("SEND_PUSHOVER"))
sendEmail = str_to_bool(os.getenv("SEND_EMAIL"))

### Pushover Config
pushoverAppToken = os.getenv("PUSHOVER_APP_TOKEN")
pushoverUserToken = os.getenv("PUSHOVER_USER_TOKEN")

### Email Config
yourEmail = os.getenv("RECEIVING_EMAIL_ADDRESS")
emailUserName = os.getenv("EMAIL_ACCESS_USERNAME")
emailPassword = os.getenv("EMAIL_ACCESS_PASSWORD")

### Link Config
link = str(os.getenv("KSL_SEARCH_LINK"))
print(os.getenv("USING_DOCKER"))

opts = Options()
opts.add_argument("--no-sandbox") #This make Chromium reachable
opts.set_headless()
opts.add_argument("--enable-javascript")

assert opts.headless
if str_to_bool(os.getenv("USING_DOCKER")):
	browser = Chrome(options=opts, executable_path='/usr/bin/chromedriver')
else:
	browser = Chrome(options=opts)
jsonListings = []
toPrint = []
print("loading")
browser.get(link)
print("finished Loading")
listings = browser.find_elements_by_class_name('listing-item')


for list in listings:
	is_featured = "featured" in list.get_attribute("class")
	if is_featured:
		continue
	listArray = {}
	listArray["link"] = list.find_element_by_class_name("listing-item-link").get_attribute('href')
	listArray["title"] = list.find_element_by_class_name("item-info-title-link").text
	listArray["price"] = list.find_element_by_class_name("item-info-price").text
	listArray["img"] = "https:" + list.find_element_by_tag_name('img').get_attribute('src')
	listArray["address"] = list.find_element_by_class_name('address').text
	jsonListings.append(listArray)


with open(FILENAME, "r+") as itemsFile:
	if itemsFile.readline().rstrip() != "":
		itemsFile.seek(0, 0)
		item = json.loads(itemsFile.readline().rstrip())
	else:
		item = {}
		item["title"] = 0
	itemsFile.seek(0, 0)

	for listing in jsonListings:
		if item["title"] == listing["title"]:
			break
		else:
			toPrint.append(listing)
	if len(toPrint) > 0:
		content = itemsFile.read()
		itemsFile.seek(0, 0)
		for listing in toPrint:
			print(json.dumps(listing, sort_keys=True), file=itemsFile)
		itemsFile.write(content)

	itemsFile.close()
# you can customize this to be whatever email you want
if len(toPrint) > 0:
	# Price - listingTitle 
	for listing in toPrint:
		

		title = "Title: " + str(listing["title"]) + "\n"
		price = "Price: " + str(listing["price"]) + "\n"
		address = "Location: " + str(listing["address"]) + "\n"
		link = str(listing["link"]) + "\n"


		msg = MIMEMultipart('alternative')

		msg['Subject'] = str(listing["price"]) + " - " + str(listing["title"])
		msg['From'] = yourEmail
		msg['To'] = yourEmail


		text =  link + title + price + address
		htmlStart = "<html><head></head><body>"
		htmlEnd = "</body></html>"


		body = """
	<a href="{link}">
		<img alt='{title}' src="{img}">
	</a>
	<h1>{title}</h1>
	<h2>Price: {price}</h2>
	<h2>Location: {address}</h2>
""".format(link=listing["link"], img=listing["img"], title=listing["title"], price=listing["price"], address=listing["address"])

		

		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(htmlStart + body + htmlEnd, 'html')

		msg.attach(part1)
		msg.attach(part2)

		if sendEmail:
			server = smtplib.SMTP( "smtp.gmail.com", 587 )
			server.ehlo()
			server.starttls()
			server.login( emailUserName, emailPassword )
			server.sendmail(yourEmail, yourEmail, msg.as_string())
		if usePushover:
			conn = http.client.HTTPSConnection("api.pushover.net:443")
			conn.request("POST", "/1/messages.json",
			urllib.parse.urlencode({
				"token": pushoverAppToken,
				"user": pushoverUserToken,
				"message": text,
				"title": str(listing["price"]) + " - " + str(listing["title"]),
			}), { "Content-type": "application/x-www-form-urlencoded" })
			conn.getresponse()
browser.close()
browser.quit()