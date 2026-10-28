#start with light weight python image
#This gives our container a python runtime
FROM python:3.11-slim

#set the working directory inside the container 
WORKDIR /app

COPY requirements.txt .

#if model is in cache take that from there here we are not using 
# avoid retaining pip's download cache in the image 
RUN pip install --no-cache-dir -r requirements.txt

#copy the application code and saved into /app fisrt dot source and second for destination[.]
COPY . . 

EXPOSE 8000
#0.0.0.0 allowing all connection through container the containers network interface
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]