FROM python:3.8-slim

COPY ./assignment_4.py /opt
COPY ./allegiance.csv /opt
COPY ./templates/* /opt/templates/

RUN pip install flask
CMD python3 /opt/assignment_4.py
