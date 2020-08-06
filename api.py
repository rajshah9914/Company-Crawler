from selenium import webdriver
from bs4 import BeautifulSoup
import time

DRIVER_PATH = 'chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
url='https://www.flipkartcareers.com/#!/job-view/senior-manager-bangalore-karnataka-2020071019410853'
driver.get(url)
time.sleep(10)
content = driver.page_source
# print(content)
# time.sleep(10)
soup = BeautifulSoup(content,"lxml")
role=soup.findAll('h2')
# ss=soup.span["data-ph-id"]
print(role[0].text)

info=soup.findAll('p',{'class':'para-text-new ng-binding'})
# print(info)
open_pos=info[1].text
req_skills=info[2].text
quali=info[4].text
exp=info[6].text

raw_data=[]
maps={'Role':role[0].text,'OpenPositions':open_pos,'ReqSkills':req_skills,'Qualification':quali,'Exp':exp}
print(maps)
raw_data.append(maps)
print(raw_data)