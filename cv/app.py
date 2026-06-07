from flask import Flask, request, jsonify

from ocr import run_ocr
from parser import analyze_document

app = Flask(__name__)


@app.route("/cv/analyze", methods=["POST"])
def analyze_cv_document():

    try:

        # Check file
        if "file" not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file uploaded."
            }), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({
                "status": "error",
                "message": "No file selected."
            }), 400

        # Read image bytes
        image_bytes = file.read()

        # OCR Extraction
        extracted_text = run_ocr(image_bytes)

        if not extracted_text:
            return jsonify({
                "status": "error",
                "message": "OCR failed. No text extracted."
            }), 500

        # Document Classification
        result = analyze_document(extracted_text)

        # Add OCR text in response
        result["extracted_text"] = extracted_text

        return jsonify(result), 200

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/")
def home():
    return {
        "message": "Sprint 5 CV Module API Running"
    }


app.run(
    host="0.0.0.0",
    port=5000,
    debug=True,
    use_reloader=False
)