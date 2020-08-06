from flask import Flask
app = Flask(__name__)
import gunicorn
from flask import render_template,jsonify
import os
from flask import url_for, redirect,request

from selenium import webdriver
from bs4 import BeautifulSoup
import time

DRIVER_PATH = 'chromedriver'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

@app.route('/')
def main():
    return render_template('home.html')

@app.route('/tesco',methods=['GET', 'POST'])
def tesco():

    list_urls={'Data':'https://www.tesco-careers.com/technology/uk/en/c/data-jobs',
    'Infrastructure':'https://www.tesco-careers.com/technology/uk/en/c/infrastructure-jobs',
    'Product':'https://www.tesco-careers.com/technology/uk/en/c/product-jobs',
    'Programme':'https://www.tesco-careers.com/technology/uk/en/c/programme-jobs','Security':'https://www.tesco-careers.com/technology/uk/en/c/security-jobs',
    'Software Engineering':'https://www.tesco-careers.com/technology/uk/en/search-results?category=Software Engineering','Software Engineering Architect':'https://www.tesco-careers.com/technology/uk/en/c/software-engineering-architecture-jobs',
    'System Engineering':'https://www.tesco-careers.com/technology/uk/en/search-results?category=System Engineering',
    'UI/UX':'https://www.tesco-careers.com/technology/uk/en/c/uiux-design-jobs',
    'Others':'https://www.tesco-careers.com/technology/uk/en/c/other-jobs'}

    roles=[]
    mapping={}
    for iterator in list_urls:
        url=list_urls[iterator]
        roles=[]
        populate=[]
        driver.get(url)
        time.sleep(1)
        content = driver.page_source
        print(content)
        # time.sleep(10)
        soup = BeautifulSoup(content,"lxml")
        s=soup.findAll('span')
        # ss=soup.span["data-ph-id"]
        for i in s:
            # print(i)
            # print(i.attrs)
            if('data-ph-id' in i.attrs):
                if(i.attrs['data-ph-id']=='ph-page-element-page1-mafXOp' or i.attrs['data-ph-id']=='ph-page-element-page24-ywciEL'):
                    print(i.text)
                    roles.append(i.text)
        populate.append(url)
        populate.append(roles)
        mapping[iterator]=populate
        # time.sleep(10)

    print(mapping)
    # data=[]
    # data.append(mapping)
    return render_template('tesco.html',data=mapping)


@app.route('/flipkart',methods=['GET', 'POST'])
def flipkart():
    url='https://www.flipkartcareers.com/#!/joblist'
    driver.get(url)
    time.sleep(10)
    content=driver.page_source
    soup1=BeautifulSoup(content,"lxml")
    xx=soup1.findAll('li',{"class": "ng-scope"})
    print(len(xx))
    # for index in range(1,len(xx)+1):
    #     url_home='https://www.flipkartcareers.com/#!/joblist'
    #     driver.get(url_home)
    #     a=driver.find_element_by_link_text(str(index))
    #     # print(a)
    #     a.click()
    #     time.sleep(20)
    raw_data=[]
    for index in range(1,len(xx)+1):
        url_home='https://www.flipkartcareers.com/#!/joblist'
        driver.get(url_home)
        time.sleep(3)
        a=driver.find_element_by_link_text(str(index))
        # print(a)
        a.click()
        content=driver.page_source
        soup=BeautifulSoup(content,"lxml")
        list_urls=[]
        x=soup.findAll('div',{"class": "col-md-4 ng-scope"})
        for a_tags in x:
            zz=a_tags.findAll('a')
            # print(zz[0])
            # print(zz[0]['href'])
            url_construct='https://www.flipkartcareers.com/'+zz[0]['href']
            list_urls.append(url_construct)
        print(list_urls)
        # list_urls=['https://www.flipkartcareers.com/#!/job-view/senior-manager-bangalore-karnataka-2020071019410853',
        # 'https://www.flipkartcareers.com/#!/job-view/manager-bangalore-karnataka-2020062312304473',
        # 'https://www.flipkartcareers.com/#!/job-view/architect-bangalore-karnataka-2020012921042577',
        # 'https://www.flipkartcareers.com/#!/job-view/associate-director-dc-ops-large-kolkata-kolkata-west-bengal-2019080914343317']
        for url in list_urls:
            driver.get(url)
            time.sleep(2)
            content = driver.page_source
            # print(content)
            # time.sleep(10)
            soup = BeautifulSoup(content,"lxml")
            role=soup.findAll('h2')
            # ss=soup.span["data-ph-id"]
            print(role[0].text)

            info=soup.findAll('p',{'class':'para-text-new ng-binding'})
            print(info)
            open_pos=info[1].text
            # req_skills=info[2].text
            # quali=info[4].text
            exp=info[len(info)-1].text

            maps={
            'Role':role[0].text,
            'OpenPositions':open_pos,
            # 'ReqSkills':req_skills,
            # 'Qualification':quali,
            'Exp':exp,
            'Link':url
            }
            print(maps)
            # maps=jsonify(maps)
            raw_data.append(maps)
    # raw_data=jsonify(raw_data)
    return render_template('flipkart.html',data=raw_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3098))
    app.run(host='0.0.0.0', port=port)