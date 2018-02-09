import os
import PyPDF2

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

home = os.path.dirname(os.path.realpath(__file__))
pdfDir = os.path.join(home, "AmericanArchivist")
outDir = os.path.join(home, "text")
if not os.path.isdir(outDir):
	os.makedirs(outDir)

for year in os.listdir(pdfDir):
	vol = os.path.join(pdfDir, year)
	for issue in os.listdir(vol):
		issuePath = os.path.join(vol, issue)
		issueName = year + "_" + issue
		print (issueName)
		outputFile = os.path.join(outDir, issueName + ".txt")
		
		issueKeywords = []
		for root, sections, files in os.walk(issuePath):
			for file in files:
				filePath = os.path.join(root, file)
				print ("	reading " + file + "...")
				pdf = open(filePath, 'rb')
				pdfReader = PyPDF2.PdfFileReader(pdf)
				pageCount = pdfReader.numPages
				count = 0
				text = ""
				while count < pageCount:
					pageObj = pdfReader.getPage(count)
					count +=1
					text += pageObj.extractText()
					
					if text != "":
						
						tokens = word_tokenize(text)
						punctuations = ['(',')',';',':','[',']',',']
						stop_words = stopwords.words('english')
						keywords = [word for word in tokens if not word in stop_words and not word in punctuations]
						for word in keywords:
							issueKeywords.append(word)
				pdf.close()
		output = open(outputFile, 'w', encoding='utf-8')
		outText = "\n".join(issueKeywords)
		output.write(outText)
		output.close()