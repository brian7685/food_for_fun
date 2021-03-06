# This is modified from https://github.com/wy36101299/PTTcrawler
# coding=UTF-8
import re
import os
import sys
import random
import json
import requests
import urllib2
from Queue import Queue
from threading import Thread
from time import sleep
from bs4 import BeautifulSoup  


def crawler(start,end):
	page = start; times = end-start+1; g_id = 0;
	for a in range(times):
		print('index is '+ str(page))
		resp = requests.get(
		url="http://www.ptt.cc/bbs/Food/index"+str(page)+".html")
		#cookies={"over18": "1"}
		#)
		soup = BeautifulSoup(resp.text)
		for tag in soup.find_all("div","r-ent"):
			try:
				link = str(tag.find_all("a"))
				link = link.split("\"")
				link = "http://www.ptt.cc"+link[1]
				g_id = g_id+1
				parseGos(page,link,g_id)
			except:
			    pass
		
		sleep(10)
		page += 1

def parseGos(page, link , g_id):
	global taipei_idx
	resp = requests.get(url=str(link),cookies={"over18":"1"})
	soup = BeautifulSoup(resp.text)
	# author
	author  = soup.find(id="main-container").contents[1].contents[0].contents[1].string.replace(' ', '')
	# print 'author:%s' %author
	# title
	title = soup.find(id="main-container").contents[1].contents[2].contents[1].string.replace(' ', '')
	# print 'title:%s' %title
	# print soup.find(id="main_container").contents[1]
	if u'台北' not in title:
		return
	# print 'title:%s' %title
	# date
	date = soup.find(id="main-container").contents[1].contents[3].contents[1].string
	# print 'date:%s' %date
	# ip
	try:
		ip = soup.find(text=re.compile("※ 發信站:"))
		ip = re.search("[0-9]*\.[0-9]*\.[0-9]*\.[0-9]*",str(ip)).group()
	except:
		ip = "ip is not find"
	# content
	a = str(soup.find(id="main-container").contents[1])
	a = a.split("</div>")
	a = a[4].split("<span class=\"f2\">※ 發信站: 批踢踢實業坊(ptt.cc),")
	content = a[0]
	content = re.sub('<.*?>','',content)
	output_file = sys.argv[3] + '/' + str(page) + '_' + str(taipei_idx) + '.txt'
	print 'process %s...' %output_file
	with open(output_file,'w') as f:
		f.write(author.encode('utf-8'))
		f.write('\n')
		f.write(title.encode('utf-8'))
		f.write('\n')
		f.write(date.encode('utf-8'))	
		f.write('\n')
		f.write(content)

	taipei_idx += 1

if __name__ == '__main__':
	taipei_idx = 1
	crawler(int(sys.argv[1]),int(sys.argv[2]))
