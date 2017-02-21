from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import time
import json
from pprint import pprint
from bs4 import UnicodeDammit
from random import randint
import codecs
from final import final
import os

class bower:
    def __init__(self):
        self.tst = final()

    def browser(self):
        #weblist = []
        #just test we will get web url.
        f = open('web.txt','w')
        #pa =open('page.txt','w')
        url = 'https://www.google.com/searchbyimage?&image_url=http://linux1.cs.utaipei.edu.tw/~u10116035/lol.jpg'
        #url = 'https://www.google.com/searchbyimage?&image_url=http://i.imgur.com/32z74Ka.jpg'
        headers = {}
        headers['User-Agent']="Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        for i in range(2):
            request = urllib.request.Request(url+'&start=' + str(i*10), headers=headers)
            response = urllib.request.urlopen(request)
            page = response.read()
            #pa.write(page.decode('utf-8'))
            #pa.close()
            #print(page)
            soup = BeautifulSoup(page,'html5lib')
            if len(soup.select('.rc h3 a')) > 0:
                print('have something in browser')
                for ele in soup.select('.rc h3 a'):
                    f.write(ele['href'] + '\n')
                    print (ele['href'])
            else:
                print('null')
                f.write('null')
                break
        f.close()
        print ('brower done!')
        self.tst.dir()
