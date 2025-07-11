FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt && echo "force rebuild"

CMD ["python", "-u", "run.py"]