FROM python:3.11.2-slim-bullseye
COPY gss/ src/
RUN pip install --upgrade pip && pip install -r src/requirements.txt
RUN mkdir -p /.secret
ENTRYPOINT ["python", "/src/main.py"]
