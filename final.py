import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import time
import requests
import json
from random import randint
import string
import jieba
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

#jieba.set_dictionary('jieba/dict.txt')
jieba.load_userdict("jieba/userdict.txt")
class final:
    def dir(self):
        if(not(os.path.exists('./seg'))):
            os.makedirs('seg')
        if(not(os.path.exists('./parse'))):
            os.makedirs('parse')
            self.Writefile()
        else:
            self.Writefile()

    def Writefile(self):
        web = open('web.txt','r')
        num = 1
        for i in web:
          if i != 'null':
              temp = open('./parse/' + str(num) + '.txt','w',encoding = 'utf-8')
              try:
                res = requests.get(i)
              except requests.exceptions.RequestException as e:
                print (e)
                pass
              soup = BeautifulSoup(res.text.encode('utf-8'),'html.parser')
              temp.write(soup.get_text())
              num += 1
              temp.close()
          else:
              #nullmsg = {}
              jfile = open('./public_html/a.json','w')
              #nullmsg['msg']='null'
              json.dump({'msg':'null'},jfile)
              return
        self.filename()

    def filename(self):
        filelist = os.listdir('./parse')
        result = []
        num = 1
        for fname in filelist:
            content = open('./parse/' + fname,'rb').read()
            words = jieba.cut(content, cut_all=False)

            for word in words:
                word = ''.join(word.split())
                if (word != '' and word != "\n" and word != "\n\n" and word >= u'\u4e00' and  word <= u'\u9fff'):
                    result.append(word.encode('utf-8'))

            f = open("./seg/"+ str(num) +"-seg.txt","wb")
            f.write(b' '.join(result))
            f.close()
            num +=1
            result = []
        print('parse finish')
        self.Tfidf()

    def Tfidf(self):
        filelist = os.listdir('./seg')
        path = './seg/'
        corpus = []
        tfidfdict = {}
        for i in filelist:
            ff = open(path + i,'r+',encoding='utf-8')
            content = ff.read()
            ff.close()
            corpus.append(content)

        vectorizer = CountVectorizer()
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
        word = vectorizer.get_feature_names()
        weight = tfidf.toarray()
        json1 = open('./public_html/a.json','w')
        #f = open('total.txt','w',encoding='utf-8')
        for i in range(len(weight)) :
            for j in range(len(word)) :
                getword = word[j]
                getvalue = weight[i][j]
                if getvalue != 0:  #去掉值为0的项
                    if getword in tfidfdict:  #更新全局TFIDF值
                        tfidfdict[getword] += getvalue
                    else:
                        tfidfdict.update({getword:getvalue})
        sorted_tfidf = sorted(tfidfdict.items(), key=lambda d:d[1],  reverse = True )
        abc = {}
        templist = []
        for i in range(10):
            templist.append({'text':sorted_tfidf[i][0],'value':sorted_tfidf[i][1]})
        abc['items'] = templist
        json.dump(abc,json1)
        print ('json done!')
        os.system("rm -rf seg/*")
        os.system("rm -rf parse/*")
        os.system("rm -rf public_html/tst.jpg")
        #os.system("rm -rf public_html/a.json")
