FROM python:3.11.4-slim

WORKDIR /ballAPI

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python","endpoints.py"]