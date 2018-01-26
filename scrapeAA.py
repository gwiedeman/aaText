import csv
import requests
import os
from bs4 import BeautifulSoup
import time
import sys

rootDir = os.path.dirname(os.path.realpath(__file__))
aaDir = os.path.join(rootDir, "AmericanArchivist")
csvFile = os.path.join(rootDir, "AmericanArchivist.csv")

headers = {'User-Agent': 'Mozilla/5.0'}
session = requests.Session()

r = session.get('http://americanarchivist.org/loi/AARC', headers=headers)
print (r.status_code)
html = r.text
soup = BeautifulSoup(html, "html.parser")

if not os.path.isdir(aaDir):
    os.makedirs(aaDir)

csvHead = ["year", "volume", "issue", "type",
           "authors", "title", "doi", "url", "path"]
outFile = open(csvFile, "w", newline='', encoding="utf8")
writer = csv.writer(outFile, delimiter=",")
writer.writerow(csvHead)
outFile.close()

articleTree = soup.find('ul', {'class': 'loiList decadeList'})
decades = articleTree.findChildren()
for decade in reversed(decades):
    liClass = decade.get('class', [])
    if "loiListHeading" in liClass:
        decadeText = decade.text
        if "Volume" in decadeText:
            volume = "Vol" + decadeText.split("Vol")[1].split(" (")[0]
            year = decadeText.split(" (")[1].split(")")[0]
            yearFolder = os.path.join(aaDir, year + " " + volume)
            print (year)
            if int(year) > 1900:
                issueList = decade.findNext('li')
                for issue in issueList.findChildren():
                    if "Issue" in issue.text:
                        if issue.name == "a":
                            issuePath = os.path.join(
                                yearFolder, issue.text.replace("/", "-"))

                            time.sleep(5)
                            session = requests.Session()
                            issuePage = session.get(
                                issue['href'], headers=headers)
                            print (issuePage.status_code)
                            if int(issuePage.status_code) == 403:
                                sys.exit()
                            else:

                                issueHtml = issuePage.text
                                issueSoup = BeautifulSoup(
                                    issueHtml, "html.parser")
                                articles = issueSoup.find_all(
                                    'table', {'class': 'articleEntry'})
                                for article in articles:
                                    time.sleep(5)
                                    typeHeading = article.findPrevious(
                                        'h2', {'class': 'tocHeading'})
                                    if int(year) > 2014:
                                        type = typeHeading.find(
                                            "span").text.strip().title()
                                    else:
                                        type = typeHeading.find(
                                            "div").text.strip().title()

                                    articleRow = [
                                        year, volume, issue.text, type]

                                    typeDir = os.path.join(
                                        issuePath, type.replace(":", "_")).replace(" ", "_")
                                    title = article.find(
                                        'div', {'class': 'art_title'}).text
                                    if not "editorial policy" in title.lower():
                                        #print (title.encode("utf8"))
                                        authors = article.find_all(
                                            'span', {'class': 'hlFld-ContribAuthor'})
                                        authorList = []
                                        for author in authors:
                                            if len(authorList) > 0:
                                                authorList.append("|")
                                            authorList.append(author.text)
                                        articleRow.append("".join(authorList))
                                        articleRow.append(title)
                                        url = "http://www.americanarchivist.org" + \
                                            article.find('a', {'title': 'Opens new window'})[
                                                "href"]
                                        doi = url.split("/pdf/")[1]
                                        articleRow.append(doi)
                                        articleRow.append(url)
                                        path = os.path.join(
                                            typeDir, doi.split("/")[1] + ".pdf")
                                        articleRow.append(path)
                                        if not os.path.isdir(typeDir):
                                            os.makedirs(typeDir)

                                        # download pdf
                                        print ("	Downloading " +
                                               str(title.encode("utf8")) + "...")
                                        session = requests.Session()
                                        pdfResponse = session.get(
                                            url, headers=headers)
                                        with open(path, 'wb') as pdf:
                                            pdf.write(pdfResponse.content)

                                        outFile = open(
                                            csvFile, "a", newline='', encoding="utf8")
                                        writer = csv.writer(
                                            outFile, delimiter=",")
                                        writer.writerow(articleRow)
                                        outFile.close()
