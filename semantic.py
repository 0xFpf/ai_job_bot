from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import requests
from time import sleep
import utils
from dotenv import dotenv_values


currPath=os.getcwd()
model = SentenceTransformer(currPath+"\\"+'MiniLM')
config = dotenv_values(".env")

botkey = config["TG_API"]
chatid = config["TG_CHATID"]


def get_similarities(json_data, cv, threshold):
    cv_emb = model.encode(cv)
    for item in json_data:
        item_desc=item['description']
        job_emb=model.encode(item_desc)
        sleep(1)
        try:
            percentage=compare_jobposts(cv_emb, job_emb)
            if percentage >= threshold:
                url=item['url']
                tgram=f"Job found, {percentage}% match: {url}"
                print(tgram)
                msg = f'https://api.telegram.org/bot{botkey}/sendMessage?chat_id={chatid}&text="{tgram}"'

                try:
                    resp=requests.get(msg)
                    # print(resp)
                except Exception as e:
                    print(e)

        except Exception as e:
            print(f"Error {e}")
            break



def compare_jobposts(cv_emb, job_emb):
    similarity=cosine_similarity(
                    [cv_emb],
                    [job_emb]
                )
    sim=similarity[0][0]
    percentage = round(sim * 100, 2)
    return percentage




if __name__ == '__main__':
    threshold=35
    pdf_path = currPath+"\\"+'CV24.pdf'
    indeed_path = currPath+"\\"+'updated_data.json'
    cv=utils.extract_text_from_pdf(pdf_path)
    json_data=utils.import_json_file(indeed_path)
    get_similarities(json_data, cv, threshold)


