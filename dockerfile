FROM python:3.10

WORKDIR /Homework

COPY . .

RUN pip install -r requirements.txt


ENTRYPOINT ["python", "./main.py" ]