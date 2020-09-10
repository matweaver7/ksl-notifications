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
import urllib.request
from urllib.parse import urlparse	

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
noImagePhrase = "noimage-bike"

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

		text  = """
	<a href="{link}">{title}</a>
	{price}
	{address}
""".format(link=listing["link"], title=title, price=price, address=address)

		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(htmlStart + body + htmlEnd, 'html')

		msg.attach(part1)
		msg.attach(part2)

		if sendEmail:
			print("Sending Email!")
			server = smtplib.SMTP( "smtp.gmail.com", 587 )
			server.ehlo()
			server.starttls()
			server.login( emailUserName, emailPassword )
			server.sendmail(yourEmail, yourEmail, msg.as_string())
		if usePushover:
			print("Sending Pushover!")
			img_filename = urlparse(listing["img"]).path.split("/")[-1]
			session = requests.Session()
			session.headers.update({
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
				'Accept-Language': 'en-US,en;q=0.5',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Connection': 'keep-alive',
				'Cache-Control': 'max-age=0',
				'Upgrade-Insecure-Requests': '1'
			})
			
			if noImagePhrase in img_filename:
				r = session.post("https://api.pushover.net/1/messages.json", data = {
						"token": pushoverAppToken,
						"user": pushoverUserToken,
						"html": 1,
						"message": text,
						"title": str(listing["price"]) + " - " + str(listing["title"])
				})
			else:
				r = session.get(listing["img"], timeout=0.5)
				if r.status_code == 200:
					with open(ROOT_DIR + "/" + img_filename, 'wb') as f:
						f.write(r.content)
				r = session.post("https://api.pushover.net/1/messages.json", data = {
					"token": pushoverAppToken,
					"html": 1,
					"user": pushoverUserToken,
					"message": text,
					"title": str(listing["price"]) + " - " + str(listing["title"]),
				},
				files = {
					"attachment": ("image.jpg", open(ROOT_DIR + "/" + img_filename, "rb"), "image/jpeg")
				})
				os.remove(ROOT_DIR + "/" + img_filename)
browser.close()
browser.quit()