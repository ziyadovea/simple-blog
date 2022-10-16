FROM python:3.10-alpine

WORKDIR app
COPY ./ ./

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]