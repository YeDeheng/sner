from lxml import html
import requests
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

link = []
j = 2

textfile = file('JavaFrameworks.txt','wt')

url = ["https://github.com/akullpp/awesome-java"] 

for x in range(51):
    link.append("//article[@class='markdown-body entry-content']/ul["+str(j)+"]/li/a/text()")
    j+=1
    
for u in url:
    thisurl = requests.get(u)        
    tree = html.fromstring(thisurl.text)
    for y in link:
        api = tree.xpath(y)
        for i in api:
            textfile.write(i+'\n')
            
textfile.close()
        


