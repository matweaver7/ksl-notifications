from pprint import pprint
filename = "carList.txt"
with open(filename, "r+") as carsFile:
	pprint(carsFile.readline())
	carsFile.seek(0,0)
