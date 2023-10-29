FROM python:3.8

RUN pip install pillow

ADD clientHTTP.py .

CMD ["python", "clientHTTP.py"]
