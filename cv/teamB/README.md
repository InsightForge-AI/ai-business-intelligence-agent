# 🧠 CV Pipeline - Image Analysis API

## 📌 Overview

This project implements a Computer Vision (CV) pipeline that performs: -
Object Detection - Optical Character Recognition (OCR) - Image
Captioning

The pipeline is exposed through a FastAPI endpoint.

------------------------------------------------------------------------

## 🚀 Features

-   Detect objects from input image
-   Extract text using OCR (EasyOCR)
-   Generate image description (captioning)
-   REST API using FastAPI

------------------------------------------------------------------------

## 📁 Project Structure

cv/teamB/ ├── app.py ├── integration/ │ └── main.py ├──
object_detection/ ├── ocr/ ├── captioning/ ├── data/ │ ├── raw/ │ └──
processed/ ├── requirements.txt └── README.md

------------------------------------------------------------------------

## ⚙️ Installation

``` bash
git clone <repo-url>
cd ai-business-intelligence-agent
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ▶️ Run the API

``` bash
uvicorn app:app --reload
```

Open: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## 📤 API Endpoint

POST /cv/analyze

------------------------------------------------------------------------

## 📥 Sample Response

{ "image": "image1.png", "objects": \["person", "car"\],
"extracted_text": \["sample text"\], "description": "A person standing
near a car" }

------------------------------------------------------------------------

## 🧪 Testing

-   Tested using Swagger UI
-   Output saved in processed folder

------------------------------------------------------------------------

## ✅ Status

✔️ CV pipeline implemented\
✔️ FastAPI integration completed\
✔️ API contract followed

------------------------------------------------------------------------

## 👩‍💻 Author

TeamB - CV Module
