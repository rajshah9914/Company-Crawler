from flask import Flask
app = Flask(__name__)
import gunicorn
from flask import render_template,jsonify
import os
from flask import url_for, redirect,request


from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

@app.route('/amazon',methods=['GET', 'POST'])
def amazon():
    raw_data=[]
    positions=["Professionals","Students and Graduates"]
    urls=["https://www.amazon.jobs/en/teams/engineering-fulfillment","https://www.amazon.jobs/en/business_categories/student-programs"]
    for index in range(0,len(urls)):
        url=urls[index]
        driver.get(url)
        time.sleep(5)
        a=driver.find_elements_by_class_name('page-button')[-1].text
        xx=int(a)
        print(xx)
        job_list=driver.find_elements_by_css_selector('h3.job-title')
        job_links=driver.find_elements_by_css_selector('a.job-link')
        for ind in range(0,len(job_list)):
            maps={
                'Criteria':positions[index],
                'role':job_list[ind].text,
                'link':job_links[ind].get_attribute('href')
            }
            raw_data.append(maps)
        # print(xx)
        for i in range(1,xx):
            # https://www.amazon.jobs/en/teams/engineering-fulfillment?offset=10&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&
            url=urls[index]+'?offset='+str(10*i)+'&result_limit=10&sort=relevant&distanceType=Mi&radius=24km&latitude=&longitude=&loc_group_id=&loc_query=&base_query=&city=&country=&region=&county=&query_options=&'
            driver.get(url)
            # print(url)
            time.sleep(5)
            job_list=driver.find_elements_by_css_selector('h3.job-title')
            job_links=driver.find_elements_by_css_selector('a.job-link')
            for ind in range(0,len(job_list)):
                maps={
                    'Criteria':positions[index],
                    'role':job_list[ind].text,
                    'link':job_links[ind].get_attribute('href')
                }
                raw_data.append(maps)
    return render_template('amazon.html',data=raw_data)
    
@app.route('/walmart',methods=['GET', 'POST'])
def walmart():
    url="https://careers.walmart.com/"
    driver.get(url)
    time.sleep(5)
    driver.find_element_by_xpath('/html/body/main/section[1]/div[2]/div/form/div[1]/div[3]/input').click()
    categories=driver.find_elements_by_css_selector('a.department-grid__link')
    links=[]
    # areas=[]
    for category in categories:
        # print(i.get_attribute('href')[28:38])
        if(category.get_attribute('href')[28:38]=="technology"):
            links.append(category.get_attribute('href'))
            # areas.append(category.text)
    # print(areas)
    raw_data=[]
    for ind in range(0,len(links)):
        driver.get(links[ind])
        title=links[ind][39:]
        print(title)
        time.sleep(2)
        # title=areas[ind]
        if(title=="information-technology"):
            go_to_jobs=driver.find_element_by_link_text("See All Openings")
            go_to_jobs.click()
            time.sleep(3)
            url_ch=driver.current_url
            # driver.find_element_by_xpath('/html/body/main/section/div/div/div[1]/form/div[1]/div[3]/input').click()
            # time.sleep(3)
            # title=driver.find_element_by_css_selector('h1.hero__title hero-title hero-title--fluid').text
            tot_jobs=driver.find_element_by_id('count_totalResults').text
            if(tot_jobs!=''):
                tot_jobs=int(tot_jobs)
            else:
                tot_jobs=int(0)
            if(tot_jobs%25==0):
                pages=tot_jobs//25
            else:
                pages=tot_jobs//25
                pages+=1
            for i in range(0,len(url_ch)):
                if(url_ch[i]=='e' and url_ch[i+1]=='='):
                    construct_url=url_ch[:i+2]
                    pos=i+2
                    break
            for i in range(pos,len(url_ch)):
                if(url_ch[i]=='&'):
                    pos2=i
                    break
            count=int(0)
            for i in range(1,pages+1):
                if(i>4):
                    break
                construct_url_ch=construct_url+str(i)
                construct_url_ch+=url_ch[pos2:]
                driver.get(construct_url_ch)
                time.sleep(3)
                job_info=driver.find_elements_by_css_selector('a.job-listing__link')
                for ind in range(0,len(job_info)):
                    maps={
                        'Category':title,
                        'Title':job_info[ind].text,
                        'Link':job_info[ind].get_attribute('href')
                    }
                    raw_data.append(maps)
        else:
            go_to_jobs=driver.find_element_by_link_text("See All Openings")
            go_to_jobs.click()
            time.sleep(3)
            # if(title=="cybersecurity"):
            # time.sleep(7)
            url_ch=driver.current_url
            # driver.find_element_by_xpath('/html/body/main/section/div/div/div[1]/form/div[1]/div[3]/input').click()
            # time.sleep(7)
            # title=driver.find_element_by_css_selector('h1.hero__title hero-title hero-title--fluid').text
            tot_jobs=driver.find_element_by_id('count_totalResults').text
            if(tot_jobs!=''):
                tot_jobs=int(tot_jobs)
            else:
                tot_jobs=int(0)
            if(tot_jobs%25==0):
                pages=tot_jobs//25
            else:
                pages=tot_jobs//25
                pages+=1
            for i in range(0,len(url_ch)):
                if(url_ch[i]=='e' and url_ch[i+1]=='='):
                    construct_url=url_ch[:i+2]
                    pos=i+2
                    break
            for i in range(pos,len(url_ch)):
                if(url_ch[i]=='&'):
                    pos2=i
                    break
            print(pages)
            for i in range(1,pages+1):
                # print(title)
                if(i>4):
                    break
                construct_url_ch=construct_url+str(i)
                construct_url_ch+=url_ch[pos2:]
                driver.get(construct_url_ch)
                time.sleep(9)
                job_info=driver.find_elements_by_css_selector('a.job-listing__link')
                print(len(job_info))
                for ind in range(0,len(job_info)):
                    maps={
                        'Category':title,
                        'Title':job_info[ind].text,
                        'Link':job_info[ind].get_attribute('href')
                    }
                    raw_data.append(maps)
    return render_template('walmart.html',data=raw_data)

@app.route('/cisco',methods=['GET', 'POST'])
def cisco():
    url="https://jobs.cisco.com/jobs/SearchJobs/?listFilterMode=1&21178=%5B%7B"+"%22%"+"24JSNType"+"%22%"+"3A"+"%22d"+"ataset_Option"+"%22%"+"2C%22value"+"%22%"+"3A%7B"+"%22i"+"d"+"%22%"+"3A207928%2C%22name"+"%22%"+"3Anull%7D%7D%5D&21178_format=6020&projectOffset=0"
    driver.get(url)
    tot_jobs_list=driver.find_elements_by_css_selector('a.pagination_item')
    tot_jobs=tot_jobs_list[-2].text
    tot_jobs=int(tot_jobs)
    elements=driver.find_elements_by_tag_name('td')
    links=[]
    job_titles=[]
    actions=[]
    area_of_interest=[]
    for element in elements:
        if(element.get_attribute('data-th')=="Actions"):
            actions.append(element.text)
        elif(element.get_attribute('data-th')=="Area of Interest"):
            area_of_interest.append(element.text)
        elif(element.get_attribute('data-th')=="Job Title"):
            job_titles.append(element.text)
            a_tag=element.find_element_by_tag_name('a')
            links.append(a_tag.get_attribute('href'))

    # for i in range(0,len(job_titles)):
    #     print(actions[i],job_titles[i],links[i])
    for ind in range(1,tot_jobs):
        urll="https://jobs.cisco.com/jobs/SearchJobs/?listFilterMode=1&21178=%5B%7B"+"%22%"+"24JSNType"+"%22%"+"3A"+"%22d"+"ataset_Option"+"%22%"+"2C%22value"+"%22%"+"3A%7B"+"%22i"+"d"+"%22%"+"3A207928%2C%22name"+"%22%"+"3Anull%7D%7D%5D&21178_format=6020&projectOffset="+str(ind*25)
        driver.get(urll)
        time.sleep(2)
        elements=driver.find_elements_by_tag_name('td')
        for element in elements:
            if(element.get_attribute('data-th')=="Actions"):
                actions.append(element.text)
            elif(element.get_attribute('data-th')=="Area of Interest"):
                area_of_interest.append(element.text)
            elif(element.get_attribute('data-th')=="Job Title"):
                job_titles.append(element.text)
                a_tag=element.find_element_by_tag_name('a')
                links.append(a_tag.get_attribute('href'))

    raw_data=[]
    print(len(job_titles),len(links),len(actions),len(area_of_interest))
    # for i in area_of_interest:
    #     print(i)
    for ind in range(0,len(job_titles)):
        maps={
            'Action':actions[ind],
            'Area Of Interest':area_of_interest[ind],
            'Job Title':job_titles[ind],
            'Link':links[ind]
        }
        raw_data.append(maps)
    return render_template('cisco.html',data=raw_data)


@app.route('/target',methods=['GET', 'POST'])
def target():
    url="https://jobs.target.com/search-jobs?k=&fl=1269750#"
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME,'pagination-show-all'))).click()
    time.sleep(4)
    links=[]
    job=[]
    la=driver.find_elements_by_tag_name('a')
    for i in la:
        if(i.get_attribute('data-job-id')):
            links.append(i.get_attribute('href'))
            job.append(i.find_element_by_tag_name('h2').text)

    Category=[]
    for i in range(0,len(links)):
        driver.get(links[i])
        element=driver.find_element_by_class_name('job-date')
        Category.append(element.text[12:])
        time.sleep(3)

    raw_data=[]
    for ind in range(0,len(links)):
        maps={
            'Category':Category[ind],
            'Job Title':job[ind],
            'Link':links[ind]
        }
        raw_data.append(maps)
    return render_template('target.html',data=raw_data)

@app.route('/philips',methods=['GET', 'POST'])
def philips():
    raw_data=[]
    posts=["SDE","Service Jobs","R&D","Procurement","Finance","Engineering","Supply Chain"]
    ur=["https://www.careers.philips.com/professional/in/en/c/software-development-jobs","https://www.careers.philips.com/professional/in/en/c/service-jobs","https://www.careers.philips.com/professional/in/en/c/r-d-jobs",
    "https://www.careers.philips.com/professional/in/en/c/procurement-jobs","https://www.careers.philips.com/professional/in/en/c/finance-jobs","https://www.careers.philips.com/professional/in/en/c/engineering-jobs","https://www.careers.philips.com/professional/in/en/c/supply-chain-jobs"]
    # url="https://www.careers.philips.com/professional/in/en/c/software-development-jobs"
    for idxx in range(0,len(ur)):
        url=ur[idxx]
        driver.get(url)
        time.sleep(3)
        checkbox_check=driver.find_elements_by_class_name('result-text')
        checkbox_check[16].click()
        jobs=driver.find_element_by_class_name('text-val-results')
        # print(jobs.text)
        tot_jobs=jobs.text[:-8]
        tot_jobs=int(tot_jobs)
        # print(tot_jobs)
        no_of_pages=0
        if((tot_jobs%50)==0):
            no_of_pages=tot_jobs//50
        else:
            no_of_pages=(tot_jobs//50)+1
        for idx in range(0,no_of_pages):
            urll=url+"?from="+str(idx*50)+"&s=1"
            driver.get(urll)
            time.sleep(3)
            titles=driver.find_elements_by_css_selector('div.title')
            # category=driver.find_elements_by_css_selector('span.job-category')
            # period=driver.find_elements_by_css_selector('span.job-industry')
            lin=driver.find_elements_by_css_selector('a.au-target')
            links=[]
            for ind in range(0,len(lin)):
                if(lin[ind].get_attribute('data-ph-at-id')=='job-link'):
                    links.append(lin[ind])
            # print(len(titles),len(category),len(period),len(links))
            for i in range(0,len(titles)):
                maps={
                    'Post':posts[idxx],
                    # 'Category':category[i].text,
                    'Job Title':titles[i].text,
                    # 'Type':period[i].text,
                    'Link':links[i].get_attribute('href')
                }
                # print(titles[i].text,category[i].text,period[i].text,links[i].get_attribute('href'))
                raw_data.append(maps)
                # time.sleep(1)
    return render_template('philips.html',data=raw_data)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
