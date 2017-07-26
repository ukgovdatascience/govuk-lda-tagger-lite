"""
This module/script takes a list of urls in csv form, scrapes their text content and writes the data structure to file. 
"""   

__author__ = "Nicky Zachariou"
__copyright__ = "Government Digital Service, 02/07/2017"
 

import requests
import csv
from bs4 import BeautifulSoup
import sys

class UrlData:
    def __init__(self,url,text):
        self.url = url
        self.text = text

# allows you to pass an argument into the script
#fname = sys.argv[1]

def read_urls(fname):
    """Function that opens a csv list of urls and scrapes their content."""
    urltext = []
    with open(fname,'r') as csvfile:
        urlreader = csv.reader(csvfile, delimiter=',')
        next(urlreader) #skips header
        for url in urlreader:
            page = requests.get(url[0]) #url in first column
            soup = BeautifulSoup(page.content,'html.parser') #parse html using bs4
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()    # rip it out
            # extract all text from html 
            txt = soup.getText()
            # format string by replacing tabs, new lines and commas
            txt = txt.strip().replace("\t", " ").replace("\r", " ").replace('\n', ' ').replace(',', ' ')
            # remove remaining excess whitespace
            txt = " ".join(txt.encode('utf-8').split())
            urltext.append(UrlData(url[0],txt))
    return(urltext)

def wtf(oname):
    """Function that writes data structure to (a .csv) file."""
    f = open(oname,'w')
    f.write('url,text\n')
    for row in urltext:
        f.write(row.url+','+row.text+'\n')
    f.close()
    return(0)

# executes only if run as a script and passed two arguements (input fileneame and output filename)
if __name__ == "__main__":
    urltext = read_urls(sys.argv[1])
    wtf(sys.argv[2])

# example:
# python govuk_scraper.py input/transport.csv input/transport_urltext.csv

