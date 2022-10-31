import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains

#국내 축구 일정

driver = webdriver.Chrome()
url = f"https://sports.news.naver.com/kfootball/schedule/index"
driver.get(url)

a = driver.find_element_by_id("_monthlyScheduleList")
