FROM python:3.6

WORKDIR /var/www/perx

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY app app
COPY run.py .

CMD ["python", "run.py"]