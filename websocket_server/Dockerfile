FROM python:alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8765

CMD [ "python", "server.py" ]