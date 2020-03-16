# -*-coding:utf-8 -*-

#想要实现的功能：1.完成pixiv下载文件的一系列过程
#				2.支持登录后下载收藏的图片

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm

from urllib.parse import urljoin

from downloadpic_new import *

import time


#originalhtml=r"https://www.pixiv.net/artworks/69080429"
originalhtml=input("请输入作品单独页面地址:")
type="jpg"
#name="mikuSymphony2018"
name=input("想要保存的图片名称:")

path=r"F:\SomePythonProjects\images\\"


browser=webdriver.Chrome()

browser.get(originalhtml)

cookies={"name":"first_visit_datetime_pc","value":"2020-02-05+14%3A33%3A50"}
cookies2={"name":"tags_sended","value":"1"}
browser.add_cookie(cookies)
browser.add_cookie(cookies2)

browser.get_cookies()
#print(browser.page_source)
'''
//*[@id="root"]/div[2]/div/div/main/section/div[1]/div/div[4]/div/div/button
//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/div[4]/div/div/button/div

//*[@id="root"]/div[2]/div/div/main/section/div[1]/div/figure/div/div[1]/div/div/div/div/div

/html/body/div[3]/div/div/div/div/div/button
/html/body/div[3]/div/div/div/div/div[2]/button


//*[@id="root"]/div[1]/div/div[1]/main/section/div[1]/div/figure/div/div[2]/div[2]/a/img

//*[@id="root"]/div[1]/div/div[1]/main/section/div[1]/div/figure/div/div[2]/div[2]/a
'''

#点击查看全部
#注意等待 有可能源码还没加载完
#browser.implicitly_wait(10)

WebDriverWait(browser,40,0.2).until(
	EC.element_to_be_clickable((By.XPATH,"//*[@id=\"root\"]/div[3]/div/div[1]/main/section/div[1]/div/div[4]/div/div/button/div"))
)

target=browser.find_element_by_xpath("//*[@id=\"root\"]/div[3]/div/div[1]/main/section/div[1]/div/div[4]/div/div/button/div")	
actions=ActionChains(browser)
actions.move_to_element(target)
actions.click()
actions.perform()




'''
#点击那些莫名其妙的确认 以后大概想办法用cookie绕过
WebDriverWait(browser,5,0.2).until(
	EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div/div"))
)
actions1=ActionChains(browser)
#先点击一次大的标签 才能成功
#"继续"
target1=browser.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div")
actions1.move_to_element(target1)
actions1.click()

target1=browser.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div/button")	
actions1.move_to_element(target1)
actions1.click()
actions1.perform()

#"试试看"
WebDriverWait(browser,5,0.2).until(
	EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/div/div/div/div[2]/button"))
)
actions2=ActionChains(browser)

target2=browser.find_element_by_xpath("/html/body/div[3]/div/div/div/div/div[2]/button")	
actions2.move_to_element(target2)
actions2.click()
actions2.perform()

'''
#pixiv是动态加载的 所以点击展开后 使用js代码下拉界面到底部并等待图片加载
js=r"window.scrollTo(0,document.body.scrollHeight)"
browser.execute_script(js)

#点击"返回顶部" 让中间跳过的部分也能加载
WebDriverWait(browser,5,0.2).until(
	EC.element_to_be_clickable((By.XPATH,"//*[@id=\"root\"]/div[6]/ul/li/button"))
)
actions3=ActionChains(browser)

target3=browser.find_element_by_xpath("//*[@id=\"root\"]/div[6]/ul/li/button")	
actions3.move_to_element(target3)
actions3.click()
actions3.perform()


#pixiv每页有个图片序号标识 可以借此数目判断最后一篇图片是否加载完成
pictotaltext=browser.find_element_by_xpath("//*[@id=\"root\"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[1]/div/div/div/div/div").text

pictotal=int(pictotaltext[-1])
print(pictotal)

txtpath=__file__
txtpath=txtpath[:txtpath.rfind("\\")+1]
print(txtpath)
f=open(txtpath+"pixiv.txt","w+",encoding="utf-8")
f.write(browser.page_source)
f.close()


#直到第一张图加载出来再进行后续操作
WebDriverWait(browser,30,0.2).until(
	EC.element_to_be_clickable((By.XPATH,"//*[@id=\"root\"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[2]/div[2]/a/img"))
)
actions4=ActionChains(browser)

#直接用download由于有些加载不出来 有可能下载不完全
#download(originalhtml,type,name,0,path,browser.page_source)


#对每张图片 先将图片点大 再对图片目标页用oridown下载（pixiv的奇葩防爬虫机制）
# 后来发现需要登陆才能点开图片 所以直接在oridown中添加了referer的head参数 至少pixiv可以用这个方法通过它网站的验证了
# 然后其实就这样通过master.jpg链接下载下来的也是原尺寸
for picnum in range(pictotal):
	'''
	target4=browser.find_element_by_xpath("//*[@id=\"root\"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[2]/div[2]/a/img")	
	actions4.move_to_element(target4)
	actions4.click()
	actions4.perform()
	'''

	#使用oridown下载(点击进入后页面信息位置固定)
	
	#//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[2]/div[2]/a/img
	#//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[3]/div[2]/a/img
	#//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[4]/div[2]/a/img
	
	pichref=browser.find_element_by_xpath("//*[@id=\"root\"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div["+str(2+picnum)+"]/div[2]/a/img")
	pichtml=pichref.get_attribute("src")
	oridown(originalhtml,pichtml,type,name,picnum,path)

	if picnum==pictotal-1:
		break

	#点击翻页键切换图片（最后一张图片不处理）
	
	#//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[10]/div/button[2]
	#//*[@id="root"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[10]/div/button[2]
	
	target4=browser.find_element_by_xpath("//*[@id=\"root\"]/div[3]/div/div[1]/main/section/div[1]/div/figure/div/div[10]/div/button[2]")	
	actions4.move_to_element(target4)
	actions4.click()
	actions4.perform()
	


'''
off=0	#偏移量

for picnum in pictotal:
	targetxpath="/html/body/div[2]/div[2]/div[4]/ul/li["+str(picnum+1)+"]/a/img"
	target=browser.find_element_by_xpath(targetxpath)	#图片的xpath
	actions=ActionChains(browser)
	actions.move_to_element(target)
	actions.click()
	actions.perform()

	handles=browser.window_handles
	handletotal=len(handles)
	browser.switch_to.window(handles[handletotal-1])

	#隐式等待
	browser.implicitly_wait(10)
	
	html=browser.current_url
	pichtml="https://fans.mihoyo.com/api/getWork?id="+html[html.rfind("=")+1:]
	
	test=requests.get(pichtml)
	#返回的是json结构，需先转换成可处理的字典格式
	pic=json.loads(test.content.decode("utf-8"))["data"]["pic_src"]
	pic=pic.replace("avatar","big")
	#print(content)
	
	off=download(pic,type,name,off)
	print("Off is:",off)
	
	browser.close()
	handles=browser.window_handles
	browser.switch_to.window(handles[0])
'''
print("准备关闭浏览器")
time.sleep(3)
browser.quit()
