from fastapi import FastAPI, UploadFile, File
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import pandas as pd
import io
import torch

app = FastAPI(title="AI CSV Analyzer API")

# ✅ Load model once
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large-cnn")

device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)


# 🔹 Universal Insight Generator
def generate_insights(df: pd.DataFrame) -> str:
    try:
        text = f"This dataset contains {len(df)} rows and {len(df.columns)} columns. "

        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        # 🔢 Numeric Insights
        if len(numeric_cols) > 0:
            text += "Key numeric insights: "
            for col in numeric_cols[:3]:
                text += (
                    f"{col} has an average of {df[col].mean():.2f}, "
                    f"minimum {df[col].min():.2f}, "
                    f"and maximum {df[col].max():.2f}. "
                )

        # 🔤 Categorical Insights
        if len(categorical_cols) > 0:
            text += "Key categorical insights: "
            for col in categorical_cols[:3]:
                try:
                    top_value = df[col].mode()[0]
                    text += f"The most common value in {col} is '{top_value}'. "
                except:
                    continue

        # 🧹 Missing values
        missing = df.isnull().sum().sum()
        text += f"There are {missing} missing values in the dataset. "

        return text

    except Exception as e:
        return f"Error generating insights: {str(e)}"


# 🔹 Summarizer (with grounding to avoid hallucination)
def get_summary(text: str) -> str:
    if not text.strip():
        return "No content to summarize."

    text = "Summarize only the following data insights. Do not add extra unrelated information: " + text

    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)

    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=120,
            min_length=40,
            num_beams=4,
            early_stopping=True
        )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


# 🔹 CSV Upload API
@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        # Read CSV safely
        df = pd.read_csv(io.BytesIO(contents), encoding='latin1')

        # Generate insights
        insights = generate_insights(df)

        # Generate summary
        # summary = get_summary(insights)

        return {
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns),
            "insights": insights,
            # "summary": summary
        }

    except Exception as e:
        return {
            "error": str(e)
        }