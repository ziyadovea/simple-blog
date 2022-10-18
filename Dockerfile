FROM python:3.10

WORKDIR app
COPY ./ ./

RUN pip install -r requirements.txt

ENV FLASK_DEBUG=1
ENV FLASK_RUN_HOST=0.0.0.0
CMD ["flask", "run"]