import json
import fitz
import re

def import_json_file(json_file):
    with open(json_file, "r") as json_file:
        data = json.load(json_file)
    return data

def export_json_file(json_file, data):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

def extract_text_from_pdf(path):
    text = ""
    with fitz.open(path) as pdf_document:
        for page_number in range(pdf_document.page_count):
            page = pdf_document.load_page(page_number)
            text += page.get_text()
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return cleaned_text