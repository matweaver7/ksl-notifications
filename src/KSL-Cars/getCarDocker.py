from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pprint

filename = "carList.txt"
yourEmail = ""
emailUserName = "YOUR USERNAME"
emailPassword = "YOUR EMAIL PASSWORD"


# Go to: https://www.ksl.com/auto/
# then enter in the search parameters you want. Then grab that url and put it here
links = "https://www.ksl.com/auto/search/index?p=&yearFrom=2011&priceTo=8000&mileageTo=120000&sellerType[]=For%20Sale%20By%20Owner&titleType[]=Clean%20Title&mileageFrom=&page=0"




server = smtplib.SMTP( "smtp.gmail.com", 587 )
server.ehlo()
server.starttls()
server.login( emailUserName, emailPassword )

opts = Options()
opts.set_headless()
opts.add_argument("--enable-javascript")
assert opts.headless
browser = Chrome(options=opts)

jsonListings = []
toPrint = []
print("loading")
browser.get(links)
print("finished Loading")
listings = browser.find_elements_by_class_name('listing')


for list in listings:
	listArray = json.loads(list.get_attribute('data-listing'))
	listArray["link"] = list.find_element_by_class_name("link").get_attribute('href')
	listArray["img"] = list.find_element_by_tag_name('img').get_attribute('src')
	listArray["index"] = "ignore"
	if listArray["regularFeatured"] != True:
		print("is not featured")
		jsonListings.append(listArray)
	else:
		print("is Featured")
		print(listArray["regularFeatured"])


with open(filename, "r+") as carsFile:
	if carsFile.readline().rstrip() != "":
		carsFile.seek(0, 0)
		car = json.loads(carsFile.readline().rstrip())
	else:
		car = {}
		car["id"] = 0
	carsFile.seek(0, 0)

	for listing in jsonListings:
		if car["id"] == listing["id"]:
			print("found")
			break
		else:
			print("not found")
			toPrint.append(listing)
	if len(toPrint) > 0:
		content = carsFile.read()
		carsFile.seek(0, 0)
		for listing in toPrint:
			print(json.dumps(listing, sort_keys=True), file=carsFile)
		carsFile.write(content)

	carsFile.close()
# you can customize this to be whatever email you want
if len(toPrint) > 0:
	for listing in toPrint:

		model = "Model: " + str(listing["makeYear"]) + " " + str(listing["model"]) + "\n"
		price = "Price: " + str(listing["price"]) + "\n"
		miles = "Miles: " + str(listing["mileage"]) + "\n"
		link = str(listing["link"]) + "\n"

		msg = MIMEMultipart('alternative')

		msg['Subject'] = str(listing["makeYear"]) + " " + str(listing["model"]) + " - " + str(listing["price"]) + " - " + str(listing["mileage"])
		msg['From'] = yourEmail
		msg['To'] = yourEmail


		text =  link + model + price + miles
		htmlStart = "<html><head></head><body>"
		htmlEnd = "</body></html>"


		body = """
	<a href="{link}">
		<img src="{img}">
	</a>
	<h1>{year} {model} {make}</h1>
	<h2>Price: {price}</h2>
	<h2>Miles: {miles}</h2>
""".format(link=listing["link"], img=listing["img"], year=listing["makeYear"], model=listing["model"], make=listing["make"], price=listing["price"], miles=listing["mileage"])

		

		part1 = MIMEText(text, 'plain')
		part2 = MIMEText(htmlStart + body + htmlEnd, 'html')

		msg.attach(part1)
		msg.attach(part2)
		server.sendmail(yourEmail, yourEmail, msg.as_string())


browser.close()
browser.quit()