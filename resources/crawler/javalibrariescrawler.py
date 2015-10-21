from lxml import html
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

textfile = file('JavaLibraries.txt','wt')

url = ["https://github.com/pditommaso/awesome-java"] 

for u in url:
    thisurl = requests.get(u)        
    tree = html.fromstring(thisurl.text)
    api = tree.xpath('//article[@class="markdown-body entry-content"]//a/text()')
    for i in api:
        textfile.write(i+'\n')
       
textfile.close()
        

