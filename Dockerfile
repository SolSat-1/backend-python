#Dockerfile
FROM python:3.9.18

WORKDIR /code 

COPY requirements.txt .  

RUN pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt 

COPY . . 

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"] 
