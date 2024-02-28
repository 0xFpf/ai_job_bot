from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import random
import time
import logging
logging.basicConfig(filename='scraper.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
import os
import utils

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
}
accept_cookies_name="Accept All Cookies"
all_data=[]


def get_details(json_data):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        for item in json_data:
            updated_desc=get_web_data(page, item['url'])
            
            item['description']=updated_desc
            all_data.append(item)
        browser.close()

        return all_data


def get_web_data(page, url):
    page.goto(url)
    page.wait_for_load_state("load")
    try:
        page_desc=get_page_data(page)
        time.sleep(random.uniform(3, 6))
        return page_desc
    except Exception as e:
        print('error')
        logging.warning(f"Error response: {e}")


def get_page_data(bsoup):
    html = bsoup.inner_html('#jobDescriptionText')
    soup = BeautifulSoup(html, 'html.parser')
    data_elements = soup.find_all(["p", "li"])
    text_combined = ""
    for p in data_elements:
        text_combined += p.get_text(strip=True) + " "
    return text_combined



if __name__ == '__main__':
    currPath=os.getcwd()
    indeed_path = currPath+"\\"+'data.json'
    json_data=utils.import_json_file(indeed_path)
    data=get_details(json_data)
    json_file = "updated_data.json"
    utils.export_json_file(json_file, data)

