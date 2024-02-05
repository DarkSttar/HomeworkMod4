FROM python:3.10

WORKDIR /Homework

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
EXPOSE 5000

ENTRYPOINT ["python", "./main.py" ]