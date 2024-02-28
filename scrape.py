from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import random
import time
import json
import logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url_techpm=str
url_softpm='https://uk.indeed.com/jobs?q=software+project+manager&l=London%2C+Greater+London&radius=10&fromage=14'
url_delivery='https://uk.indeed.com/jobs?q=delivery+manager&l=London%2C+Greater+London&radius=10&fromage=14&start=10&vjk=7b8feeeff6ab610b'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
}


accept_cookies_name="Accept All Cookies"
all_data=[]

def get_web_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=50)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)
        page.wait_for_load_state("load")
        time.sleep(3)
        page.locator("'"+accept_cookies_name+"'").click()
        
        i=0
        while True:
            # print(i)
            if i == 0:
                print(url)
                get_page_data(page)
                i+=1
                time.sleep(3)
            elif i == 1:
                url_edit=url+'&start='+str(i)+str(0)
                i+=1
                page.goto(url_edit)
                alert=check_jobalert(page)
                if alert:
                    print(url_edit)
                    get_page_data(page)
                else:
                    print('no alert found')
                    get_page_data(page)
                time.sleep(3)
            else:
                url_edit=url+'&start='+str(i)+str(0)
                i+=1
                print(url_edit)
                page.goto(url_edit)
                page.wait_for_load_state("load")
                time.sleep(random.uniform(3, 10))
                if check_lastpage(page):
                    try:
                        get_page_data(page)
                        time.sleep(random.uniform(3, 10))
                    except Exception as e:
                        json_file = "data.json"
                        with open(json_file, 'w') as file:
                            json.dump(all_data, file, indent=4)
                        logging.warning(f"Error response: {e}")
                        logging.warning(f"Page skipped: {i}")
                else:
                    json_file = "data.json"
                    with open(json_file, 'w') as file:
                        json.dump(all_data, file, indent=4)

                    browser.close()
                    break


def check_lastpage(page):
    try:
        page.wait_for_load_state("networkidle")
        tmp_html= page.inner_html('[aria-label="pagination"]')
        tmp_soup = BeautifulSoup(tmp_html, 'html.parser')
        if tmp_soup.find(attrs={"aria-label": "Next Page"}):
            return True
        else:
            print('no NEXT PAGE found')
            return False
    except Exception as e:
        print(f"Page load timed out. {e}")
        return False
    
def check_jobalert(page):
    try:
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        close_popup=page.query_selector('[aria-label="close"]')
        if close_popup:
            close_popup.click()
            return True
        else:
            return False
    except Exception as e:
            print(f"Page load timed out. {e}")
            return False

def get_page_data(bsoup):
    html = bsoup.inner_html('#mosaic-jobResults')
    soup = BeautifulSoup(html, 'html.parser')
    
    data_elements = soup.find_all(class_="job_seen_beacon")
    
    data={}

    for item in data_elements:
        title=item.find(class_="jobTitle")
        next_span = title.find_next('span')
        if next_span:
            title_text = next_span.get_text(strip=True)
        else:
            print('error, no titles found, breaking')
            break
        data['title']=title_text
        
        companyname_span = item.find('span', {'data-testid': 'company-name'})
        companyname_span=companyname_span.text.strip()

        location = item.find('div', {'data-testid': 'text-location'})
        location = location.text.strip()

        li_texts=[]
        desc_element = item.find(class_="underShelfFooter")
        if desc_element:
            for li_tag in desc_element.find_all("li"):
                li_text = li_tag.text.strip()
                li_texts.append(li_text)
            li_texts_combined = ", ".join(li_texts)
        else:
            li_texts_combined='N/A'
    
        salary_element=item.find('div', {'class': 'salary-snippet-container'})
        if salary_element:
            salary_element = salary_element.find('div', {'data-testid': 'attribute_snippet_testid'})
            salary_element = salary_element.text.strip()
        else:
            salary_element='N/A'

        url_a=item.find(class_="jobTitle")
        a_tag = url_a.find('a')
        a_tag_jk = a_tag.get('data-jk')
        a_tag_tk = a_tag.get('data-mobtk')
        a_tag=f'https://uk.indeed.com/viewjob?jk={a_tag_jk}&tk={a_tag_tk}&from=serp&vjs=3'

        row_data = {'title': title_text, 'company': companyname_span, 'location' : location, 'description':li_texts_combined, 'salary':salary_element,'url': a_tag }
        all_data.append(row_data)

    print('scrape successful')



if __name__ == '__main__':
    url=url_softpm
    get_web_data(url)
