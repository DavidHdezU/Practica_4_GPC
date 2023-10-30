FROM python:3.8

RUN pip3 install pillow
RUN pip3 install climage 

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

CMD ["python", "clientHTTP.py"]
