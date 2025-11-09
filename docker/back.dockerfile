FROM python:latest

COPY . /backend/
WORKDIR /backend

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
