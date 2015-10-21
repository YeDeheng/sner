from lxml import html
import requests
import re
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')

link = []
j = 1

textfile = file('c#Frameworks.txt','wt')

url = ["https://github.com/uhub/awesome-c-sharp"] 

for x in range(299):
    link.append("//article[@class='markdown-body entry-content']/ul/li["+str(j)+"]/a/text()")
    j+=10
    
for u in url:
    thisurl = requests.get(u)        
    tree = html.fromstring(thisurl.text)
    for y in link:
        api = tree.xpath(y)
        for i in api:
            textfile.write(i+'\n')
            
textfile.close()
        


