import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

import easyocr

reader = easyocr.Reader(['en'])

def extract_text(image_path):
    results = reader.readtext(image_path)
    
    texts = []
    for (bbox, text, confidence) in results:
        if confidence > 0.3:
            texts.append(text)
    
    return texts


def process_folder(folder_path):
    all_results = {}
    
    for filename in os.listdir(folder_path):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            full_path = os.path.join(folder_path, filename)
            extracted = extract_text(full_path)
            all_results[filename] = extracted
            print(f"{filename} -> {extracted}")
    
    return all_results

process_folder(r"D:\cv_prj\ai-business-intelligence-agent\cv\teamB\data\raw")