FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
RUN pip install --upgrade pip
COPY requirements.txt /app
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app
WORKDIR /app
CMD [ "sh", "run.sh" ]
