import scrape, scrape_posts, semantic, utils
import os
from time import sleep

url='https://uk.indeed.com/jobs?q=software+project+manager&l=London%2C+Greater+London&radius=10&fromage=14'
threshold=35
sixty_minutes=60*60
hours=24*sixty_minutes 

if __name__ == '__main__':
        
    while True:    
        # get all job posts and their links
        scrape.get_web_data(url)

        # go into each job post scraped and fetch the description
        currPath=os.getcwd()
        indeed_path = currPath+"\\"+'data.json'
        json_data=utils.import_json_file(indeed_path)
        data=scrape_posts.get_details(json_data)
        json_file = "updated_data.json"
        utils.export_json_file(json_file, data)

        # extract text from cv and send tg message to job posts with high similarity
        pdf_path = currPath+"\\"+'CV24.pdf'
        indeed_path = currPath+"\\"+'updated_data.json'
        cv=utils.extract_text_from_pdf(pdf_path)
        json_data=utils.import_json_file(indeed_path)
        semantic.get_similarities(json_data, cv, threshold)

        # set to scrape every 24 hours
        print('sleeping')
        sleep(hours)
