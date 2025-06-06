FROM python:3.10

WORKDIR /webapp_analyzer_bridge

COPY ./requirements.txt /webapp_analyzer_bridge/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /webapp_analyzer_bridge/requirements.txt

COPY ./app /webapp_analyzer_bridge/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]
