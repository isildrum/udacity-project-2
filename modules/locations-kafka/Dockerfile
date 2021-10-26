FROM python:3.8
WORKDIR .

ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# command to run on container start
CMD [ "python", "main.py" ]