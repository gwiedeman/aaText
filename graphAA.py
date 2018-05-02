import os
import json
import argparse
import sys

from nltk.tokenize import word_tokenize
import nltk
import matplotlib.pyplot as plt

argParse = argparse.ArgumentParser()
argParse.add_argument("-n", help="Phase(s) to graph, different versions separated by a pipe (|). Accepts multiple args.", action='append')
argParse.add_argument("-x", help="Value of X-Axis, supports lssue or year, and defaults to year.")
argParse.add_argument("-range", help="Range of years to include, such as: 1980-1998")
argParse.add_argument("-per", help="Instances per x number of words.")
argParse.add_argument("-input", help="Path to directory of Text files (optional).")
args = argParse.parse_args()

home = os.path.dirname(os.path.realpath(__file__))

yList = []
xLists = {}

for phrase in args.n:
	xLists[phrase] = []

if args.input:
	textDir = args.g
else:
	textDir = os.path.join(home, "text")

if not os.path.isdir(textDir):
	print ("Error: Input Directory is incorrect. Please run extractText.py or enter the path to a directory of text files after with -input.")
else:
	currentYear = ""
	yearText = ""
	xAxis = []
	text = ""
	if args.x:
		method = args.x
	else:
		method = "year"
	
	xAxis = []
	for root, dirs, files in os.walk(textDir):
		if method.lower() == "issue" or method.lower() == "issues":
			if args.range:
				r1, r2 = args.range.split("-")
				for file in files:
					fileYear = int(file.split("_")[0])
					if fileYear >= int(r1) and fileYear <= int(r2):
						xAxis.append(file)
			else:
				xAxis = files
		else:
			if args.range:
				r1, r2 = args.range.split("-")
			else:
				r1 = 1900
				r2 = 2200
			for x in range(int(r1), int(r2)):
				yearGroup = []
				for file in files:
					if file.startswith(str(x)):
						yearGroup.append(file)
				if len(yearGroup) > 0:
					xAxis.append(yearGroup)
		
		for group in xAxis:
			text = ""
			if isinstance(group, str):
				xLabel = group
				print ("Reading " + str(group) + "...")
				issuePath = os.path.join(root, group)
				textFile = open(issuePath, 'r', encoding='utf-8')
				text = textFile.read()
			else:
				for issue in group:
					xLabel = issue.split("_")[0]
					print ("Reading " + str(issue) + "...")
					issuePath = os.path.join(root, issue)
					textFile = open(issuePath, 'r', encoding='utf-8')
					text = text + "\n" + textFile.read()
						
			if text != "":
				try:
					tokens = word_tokenize(text.lower())
				except:
					nltk.download('punkt')
					tokens = word_tokenize(text.lower())
				wordCount = len(tokens)
				yList.append(xLabel)
				
				for phrase in args.n:
					xList = []
					matchCount = 0
					matchList = str(phrase).strip().lower().split("|")
					for version in matchList:
						match = tuple(version.split(" "))
						grams = nltk.ngrams(tokens, len(version.split(" ")))
						for gram in grams:
							if gram == match:
								matchCount += 1
					
						if args.per:
							yLabel = "Instances per " + str(args.per) + " Words"
							chunk = wordCount / int(args.per)
							matchCount = matchCount / chunk
						else:
							yLabel = "Instances"
						#print (phrase + ": " + str(matchCount))
					xLists[phrase].append(matchCount)
	
	#print (xLists)
	for key, line in xLists.items():
		plt.plot(yList, line, label=key.title().replace("|", " or "))			
	plt.xlabel(str(method).title())
	plt.ylabel(yLabel)
	plt.xticks(rotation="vertical")
	plt.legend(loc='upper left')
	graphTitle = "N-grams in the American Archivist"
	plt.title(graphTitle)
	plt.show()