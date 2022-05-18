FROM python:3.9-alpine
WORKDIR comics_publicist/
COPY requirements.txt .
RUN apk update && pip install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]