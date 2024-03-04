FROM python:3 
# python:3.8-slim

WORKDIR /app

# Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .
COPY . /app

# RUN pip install nodemon
# Use nodemon for watching dir and hot-reloading
RUN apt-get update
RUN apt-get install -y nodejs npm
RUN npm i -g nodemon

# Command to run the application
# CMD ["python", "main.py"]
CMD ["nodemon", "--exec", "python", "main.py"]
