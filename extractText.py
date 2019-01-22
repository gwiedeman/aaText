import os
from tika import parser
import datetime
import traceback
import argparse

argParse = argparse.ArgumentParser()
argParse.add_argument('-o', help='Will re-extract and override existing files', action='store_true')
argParse.add_argument("-range", help="Range of years to include, such as: 1980-1998")
args = argParse.parse_args()

home = os.path.dirname(os.path.realpath(__file__))

pdfDir = os.path.join(home, "AmericanArchivist")
textDir = os.path.join(home, "text")
logPath = os.path.join(home, "errors.log")
if not os.path.isdir(textDir):
    os.makedirs(textDir)

if args.range:
    r1, r2 = args.range.split("-")
else:
    r1, r2 = [1900, 2200]
for year in os.listdir(pdfDir):
    yearTest = int(year.split("_")[0])
    if yearTest < int(r1) or yearTest > int(r2):
        pass
    else:
        vol = os.path.join(pdfDir, year)
        for issue in os.listdir(vol):
            issuePath = os.path.join(vol, issue)
            issueName = year + "_" + issue
            print (issueName)
            textPath = os.path.join(textDir, issueName + ".txt")
            if os.path.isfile(textPath) and args.o == False:
                print ("    " + issueName + " already extracted.")
            else:
                text = ""
                for root, sections, files in os.walk(issuePath):
                    for file in files:
                        filePath = os.path.join(root, file)
                        print ("    reading " + file + "...")
                        parsed  = parser.from_file(filePath)
                        text = text + "\n" + parsed['content']
                            
                if text != "":
                    textFile = open(textPath, 'w', encoding='utf-8')
                    textFile.write(text)
                    textFile.close()
