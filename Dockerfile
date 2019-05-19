FROM python:3.6
WORKDIR /usr/src/web
COPY requirements.txt .
COPY index.py .
EXPOSE 4000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python","index.py"]
