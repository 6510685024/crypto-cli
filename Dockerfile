FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install python-dotenv

COPY . .

CMD ["python", "main.py", "top"] 
#Default command to run