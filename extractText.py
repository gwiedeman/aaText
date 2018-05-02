import os
from tika import parser
import datetime
import traceback

home = os.path.dirname(os.path.realpath(__file__))

pdfDir = os.path.join(home, "AmericanArchivist")
textDir = os.path.join(home, "text")
logPath = os.path.join(home, "errors.log")
if not os.path.isdir(textDir):
	os.makedirs(textDir)
	
for year in os.listdir(pdfDir):
	vol = os.path.join(pdfDir, year)
	for issue in os.listdir(vol):
		issuePath = os.path.join(vol, issue)
		issueName = year + "_" + issue
		print (issueName)
		textPath = os.path.join(textDir, issueName + ".txt")
		
		text = ""
		for root, sections, files in os.walk(issuePath):
			for file in files:
				filePath = os.path.join(root, file)
				print ("	reading " + file + "...")
				parsed  = parser.from_file(filePath)
				text = text + "\n" + parsed['content']
					
		if text != "":
			textFile = open(textPath, 'w', encoding='utf-8')
			textFile.write(text)
			textFile.close()
