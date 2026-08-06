FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file and install dependencies
COPY teamB/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "teamB.api.main:app", "--host", "0.0.0.0", "--port", "8001"]
