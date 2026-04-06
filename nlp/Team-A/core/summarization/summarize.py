import pandas as pd
from app.models.summarize_bm import get_model

tokenizer, model, device = get_model()


# 🔹 Generate Insights
def generate_insights(df: pd.DataFrame) -> str:
    try:
        text = f"This dataset contains {len(df)} rows and {len(df.columns)} columns. "

        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        # Numeric
        if len(numeric_cols) > 0:
            text += "Key numeric insights: "
            for col in numeric_cols[:3]:
                text += (
                    f"{col} has an average of {df[col].mean():.2f}, "
                    f"minimum {df[col].min():.2f}, "
                    f"and maximum {df[col].max():.2f}. "
                )

        # Categorical
        if len(categorical_cols) > 0:
            text += "Key categorical insights: "
            for col in categorical_cols[:3]:
                try:
                    top_value = df[col].mode()[0]
                    text += f"The most common value in {col} is '{top_value}'. "
                except:
                    continue

        # Missing
        missing = df.isnull().sum().sum()
        text += f"There are {missing} missing values in the dataset. "

        return text

    except Exception as e:
        return f"Error generating insights: {str(e)}"


# 🔹 Summarizer
def get_summary(text: str) -> str:
    if not text.strip():
        return "No content to summarize."

    text = "Summarize only the following data insights. Do not add extra unrelated information: " + text

    inputs = tokenizer(text, return_tensors="pt", truncation=True).to(device)

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=120,
        min_length=40,
        num_beams=4,
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)