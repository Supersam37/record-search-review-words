# -*- coding: utf-8 -*-
"""
Created on Wed Mar  7 10:45:21 2018

@author: Wangz
"""

import requests as rq
import re 
from bs4 import BeautifulSoup
import bs4

hd = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

def inputwords():
    '''
    Input words. Return list of words. Each word is of class word.
    '''
    words = []
    print(r'Enter "Q" to quit.')
    comp = re.compile('^[a-zA-Z]+$')
    while True:
        try:
            Eng_word = str(input('Enter English words:'))
            if comp.match(Eng_word) == None:
                raise ValueError
            if Eng_word == 'Q':
                break
            words.append(word(Eng_word))
            #print (words)
        except ValueError:
            print('Must be English word')
            continue
    return words

class word(object):
    '''
    Has attrs:name/basic_defination/full_defination/examples.
    '''
    def __init__(self,name):
        self.name = name
    def getname(self):
        return self.name
    def import_basic_defination(self,basic_defination):
        self.basic_defination = basic_defination
    def get_basic_defination(self):
        return self.basic_defination
    def import_full_defination(self,full_defination):
        self.full_defination = full_defination
    def get_full_defination(self):
        return self.full_defination
    def import_examples(self,examples):
        self.examples = examples
    def get_examples(self):
        return self.examples
    def import_level(self,level):
        self.level = level
    def get_level(self):
        return self.level
    def __str__(self):
        return self.name

def Lookupword_get_text(word):
    '''
    Look up the word on youdao. Get word's html text.
    '''
    word_url = 'http://dict.youdao.com/w/{0}/#'.format(word.getname())
    try :
        word_html = rq.get(word_url,headers = hd,timeout = 30)
        word_html.raise_for_status()
        word_html.encoding = word_html.apparent_encoding
        return word_html.text
    except:
        print('404 Page not found')
        
def find_defination(word,text):
    '''
    Get definations from text and bound it to word.
    '''
    full_defination = []
    soup = BeautifulSoup(text,'html.parser')
    try:
        list_full_defination = soup.find_all('div',"collinsMajorTrans")
    except:
        list_full_defination = []
    for it in list_full_defination:
        a_full_defination = {}
        try:
            List_prop = it.find_all('span','additional')
            try:
                a_full_defination['property'] = List_prop[0].string+List_prop[1].string
                prop_string1 = List_prop[0].string
                prop_string2 = List_prop[1].string
            except:
                a_full_defination['property'] = List_prop[0].string
                prop_string1 = List_prop[0].string
                prop_string2 = ''
        except:
            a_full_defination['property'] = ''
            prop_string1 = ''
            prop_string2 = ''
            
        try:
            List_def = it.find_all('p')
            def_lst = []
            for i in List_def[0].descendants:
                if type(i) == bs4.element.NavigableString:
                    i = str(i)
                    i = re.sub('[\t\n]','',i)
                    i = re.sub('^[\s]+','',i)
                    i = re.sub('[\s]+$','',i)
                    if i != '' and i != prop_string1 and i !=  prop_string2:
                        def_lst.append(i)
            conc_str  = r' " '
            def_str =conc_str.join(def_lst)
            a_full_defination['defination'] = def_str
        except:
            a_full_defination['defination'] = ''
        
        examples = []
        try:    
            for j in it.next_siblings:
                if type(j) == bs4.element.Tag:
                    one_exp = j.find_all('p')
                    one_exp_str = ''
                    for k in one_exp:
                        one_exp_str += str(k.string)
                    examples.append(one_exp_str)
        except:
            pass
        a_full_defination['examples'] = examples
        
        full_defination.append(a_full_defination)
        
    word.import_full_defination(full_defination)
    
    all_examples = []
    for i in word.get_full_defination():
        all_examples.append(i['examples'])
    word.import_examples(all_examples)
    
    basic_defination = []
    try:
        list_basic_defination = soup.find_all('div','results-content')
        list_basic_defination = list_basic_defination[0].find_all('div','trans-wrapper clearfix')
        list_basic_defination = list_basic_defination[0].find_all('div','trans-container')
        list_basic_defination = list_basic_defination[0].find_all('li')
        for i in list_basic_defination:
            basic_defination.append(str(i.string))
    except:
        pass
    word.import_basic_defination(basic_defination)
    
    return word

def main_func():
    words = inputwords()
    new_words = []
    for i in words:
        if Lookupword_get_text(i) == '404 Page not found':
            continue
        text = Lookupword_get_text(i)
        new_words.append(find_defination(i,text))
    return new_words

def basic_user():
    new_words = main_func()
    for i in new_words:
        print(i.name+':')
        print('基本释义：'+'*'*20)
        for j in i.get_basic_defination():
            print(j)
        print()
        print('柯林斯词典：'+'*'*20)
        for j in range(len(i.get_full_defination())):
            print(str(j+1)+'.',end = '')
            print('词性用法：'+i.get_full_defination()[j]['property'])
            print('解释：'+i.get_full_defination()[j]['defination'])
            print('例句：')
            for k in i.get_full_defination()[j]['examples']:
                print(k)
        print()
        print('*'*40)
            
        


     
    
    
            
            
                        
                        
        
        
                    
        
        
        
        
        
        
        
        