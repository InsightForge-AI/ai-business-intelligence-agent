import json
import os

def load_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(BASE_DIR, "data", "raw", "document.json")
    
    with open(json_path, "r") as f:
        documents = json.load(f)
    
    return documents

def save_loaded_data(documents):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Create data/cleaned/ folder if not exists
    cleaned_dir = os.path.join(BASE_DIR, "data", "cleaned")
    os.makedirs(cleaned_dir, exist_ok=True)

    # Save output as JSON inside data/cleaned/
    output_path = os.path.join(cleaned_dir, "loaded_documents.json")
    with open(output_path, "w") as f:
        json.dump(documents, f, indent=4)

    print(f"✅ Loaded data saved to: {output_path}")

if __name__ == "__main__":
    docs = load_data()
    
    # Print to terminal
    for doc in docs:
        print(doc["title"], "->", doc["category"])
    
    # Save to data/cleaned/
    save_loaded_data(docs)