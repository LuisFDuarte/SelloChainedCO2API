# 
FROM python:3.10
ENV PORT=$port
# 
WORKDIR /code

# 
COPY requirements.txt /code/
# install dependencies
RUN pip install -r requirements.txt

# copy the content of the local src directory to the working directory

ADD . .

# 
CMD ["python", "./main.py"]
