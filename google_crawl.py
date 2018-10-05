# -*- coding: utf-8 -*-
"""this script crawls google, and returns information from a user searched"""
from pyvirtualdisplay import Display
from selenium import webdriver
import re
import time
import random
import datetime
from selenium.webdriver.support.ui import WebDriverWait
import json
import os
import MySQLdb

display = Display(visible=0, size=(1200, 1000))
display.start()

chrome = webdriver.Chrome()

wait = WebDriverWait(chrome, timeout=10)
finalList = []

def google(number):
    counter=0
    chrome.get('https://www.google.com.ng')
    search = chrome.find_element_by_css_selector('#lst-ib')
    search.send_keys(number)
    googlesearch = chrome.find_element_by_name('btnK')
    googlesearch.click()
    time.sleep(2)

    page = str(chrome.page_source.encode('UTF-8'))
    myData = page.split(r'<div class="rc">')
    getInfo(myData)

    new_search = chrome.find_element_by_id('pnnext')
    while new_search:
        try:
            new_search.click()
            time.sleep(2)
            page = str(chrome.page_source.encode('UTF-8'))
            myData = page.split(r'<div class="rc">')
            getInfo(myData)
        except:
            break

    finaldata=json.dumps(finalList)
    #print(finaldata)
    return finaldata

def getInfo(myData):
    myList = []
    for item in myData:
        myDict = {}
        urls = re.findall(r'<a href="(\S*)"', item)
        titles = re.findall('ved=.+</a>?', item)
        desc = re.findall(r'class="st">(.*)</span>?', item)

        for url in urls:
            new_url = url.split('"')
            if new_url:
                myDict['URL:'] = new_url[0]

        for title in titles:
            title2 = title.split('</a>')
            search2 = re.search('">(.+)', title2[0])
            if search2:
                if not search2.group(0)[2:3] == '<' and not search2.group(0)[2:3] == ' ' and not search2.group(0)[
                                                                                                 2:8] == 'Images':
                    myDict['Title'] = search2.group(1).replace('\'','')

        for lnk in desc:
            new_desc = lnk.split('</span>')
            myDesc = new_desc[0].replace('<em>', '')
            myDesc = myDesc.replace('</em>', '')
            myDesc = myDesc.replace('<wbr>', '')
            myDesc = myDesc.replace('</wbr>', '')
            myDesc = myDesc.replace('\\', '')
            myDesc = myDesc.replace('\'', '')
            myDesc = myDesc.replace('\"', '')
            if myDesc:
                myDict['Description:'] = myDesc
                if not myDict in myList:
                    myList.append(myDict)
        
    for item in myList:
        if not len(item) == 0 and len(item) > 1:
            finalList.append(item)





