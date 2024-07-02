FROM python:3.11.4-slim

WORKDIR /ballAPI

COPY requirements.txt .

COPY . .

CMD ["python","endpoints.py"]