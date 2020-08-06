from flask import Flask
app = Flask(__name__)
import gunicorn
from flask import render_template,jsonify
import os
from flask import url_for, redirect,request

from selenium import webdriver
from bs4 import BeautifulSoup
import time


#GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
#CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.binary_location = "/app/.apt/usr/bin/google_chrome"

# driver = webdriver.Chrome(execution_path="/app/.chromedriver/bin/chromedriver", chrome_options=chrome_options)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)


##DRIVER_PATH = 'chromedriver'
##driver = webdriver.Chrome(executable_path=DRIVER_PATH)

@app.route('/')
def main():
#     driver.get("https://www.youtube.com/watch?v=NerQs_SOwRo")
    return render_template('home.html')

@app.route('/tesco',methods=['GET', 'POST'])
def tesco():

    list_urls={'Infrastructure':'https://www.tesco-careers.com/technology/uk/en/c/infrastructure-jobs',
    'Data':'https://www.tesco-careers.com/technology/uk/en/c/data-jobs',
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
        time.sleep(1.6)
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
#         time.sleep(30)

    print(mapping)
    # data=[]
    # data.append(mapping)
#     mapping = {'Data': ['https://www.tesco-careers.com/technology/uk/en/c/data-jobs', ['Senior Data Scientist']], 'Infrastructure': ['https://www.tesco-careers.com/technology/uk/en/c/infrastructure-jobs', ['Head of Service Management', 'Systems Engineer III - Networks', 'Head of Systems Engineering - Product and Architecture', 'Change and Adoption Manager, Workplace Technology', 'Product Manager - Identity & Collaboration, Workplace Technology']], 'Product': ['https://www.tesco-careers.com/technology/uk/en/c/product-jobs', ['Product Manager - Store Stock and Self Edge Management', 'Product Manager - Post Order', 'Senior Product Manager', 'Product Manager - MCA']], 'Programme': ['https://www.tesco-careers.com/technology/uk/en/c/programme-jobs', ['Technical Programme Manager - Product Transformation', 'Technical Programme Manager - Infrastructure', 'Lead Technical Programme Manager – Tesco Till Hardware and Projects', 'Senior Technical Programme Manager – Stores Hardware', 'Technical Programme Manager - Data', 'Senior Technical Programme Manager – Infrastructure']], 'Security': ['https://www.tesco-careers.com/technology/uk/en/c/security-jobs', ['Security Analyst II (IAM) – Infrastructure Controls', 'Security Analyst II (IAM) – Application Controls', 
#     'Security Engineering Manager - Cyber Platforms', 'Systems Engineer II', 'Technology Risk and Compliance Manager', 'Security Engineer - SIEM & SOC', 'Security Analyst II', 'Security Architect', 'Systems Engineering Manager']], 'Software Engineering': ['https://www.tesco-careers.com/technology/uk/en/search-results?category=Software Engineering', ['Software Dev Engineer III- Data Engineering', 'Software Dev Engineer II', 'Software Dev Engineer III', 'Software Development Manager', 'Head of Software Development', 'Systems Engineering Manager', 'Software Dev Engineer III', 'Principal Software Dev Engr', 'Software Dev Engineer III']], 'Software Engineering Architect': ['https://www.tesco-careers.com/technology/uk/en/c/software-engineering-architecture-jobs', ['Software Development Manager - Tills', 'Senior Java Engineer', 'Senior Java Developer', 'Senior Software Engineer - Frontend', 'Software Development Manager - Encryption', 'Software Development Engineer III – Android', 'Principal Software Development Engineer - Data & Analytics', 'Senior .NET Developer', 'Systems Engineer DevOps (Omnichannel)', 'Senior Developer - Tesco Connect']], 'System Engineering': ['https://www.tesco-careers.com/technology/uk/en/search-results?category=System Engineering', ['Systems Engineer II', 'Systems Engineer I - JIRA', 'Systems Engineer I', 'Systems Engineer I', 'Systems Engineer I', 'Systems Engineer II', 'Systems Engineer I', 'Systems Engineer III', 'Systems Engineer II', 'Systems Engineering Manager - Storage & Backup']], 'UI/UX': ['https://www.tesco-careers.com/technology/uk/en/c/uiux-design-jobs', ['Associate UX Designer', 'UI Designer - Complex Applications', 'Senior Product Designer']], 'Others': ['https://www.tesco-careers.com/technology/uk/en/c/other-jobs', ['Software Development Engineer III', 'Product Manager - Computer Vision', 'Product Manager - Data Platforms', 'Software Development Engineer III', 'Software Dev Engineer II', 'Senior Digital Analyst (Customer Product)', 'Head of Product - Colleague Transformation']]}
    return render_template('tesco.html',data=mapping)


@app.route('/flipkart',methods=['GET', 'POST'])
def flipkart():
    url='https://www.flipkartcareers.com/#!/joblist'
    driver.get(url)
    time.sleep(1)
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
#     xx=[1]
    for index in range(1,len(xx)+1):
        url_home='https://www.flipkartcareers.com/#!/joblist'
        driver.get(url_home)
        time.sleep(5)
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
#         list_urls=['https://www.flipkartcareers.com/#!/job-view/senior-manager-bangalore-karnataka-2020071019410853']
        # 'https://www.flipkartcareers.com/#!/job-view/manager-bangalore-karnataka-2020062312304473',
        # 'https://www.flipkartcareers.com/#!/job-view/architect-bangalore-karnataka-2020012921042577',
        # 'https://www.flipkartcareers.com/#!/job-view/associate-director-dc-ops-large-kolkata-kolkata-west-bengal-2019080914343317']
        for url in list_urls:
            driver.get(url)
            time.sleep(1.25)
            content = driver.page_source
            # print(content)
            # time.sleep(10)
            soup = BeautifulSoup(content,"lxml")
            role=soup.findAll('h2')
            # ss=soup.span["data-ph-id"]
            print(role[0].text)

            info=soup.findAll('p',{'class':'para-text-new ng-binding'})
#             print(info)
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
#             print(maps)
            # maps=jsonify(maps)
            raw_data.append(maps)
    # raw_data=jsonify(raw_data)
    return render_template('flipkart.html',data=raw_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3098))
    app.run(host='0.0.0.0', port=port)
