FROM python:latest

COPY . /backend/
WORKDIR /backend

EXPOSE 5000

RUN pip install -r requirements.txt

ENV PYTHONPATH=/backend

CMD ["python", "app.py"]
