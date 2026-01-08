# creating base image
from python:3.10-slim


# environment variables
ENV PYTHONDONTWRITEBYTECODE 1 
# Prevents Python from creating .pyc files (compiled bytecode files) Prevents creation of __pycache__

ENV PYTHONUNBUFFERED 1
#logs will be shown in real time very quick



# setting working directory
WORKDIR /app

# installing system dependencies
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

#first coping requiremnts.txt to be optimised
copy requirements.txt .

# installing python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copying project files
COPY . .

#expose FASTAPI 
EXPOSE 8000

# command to run the application
CMD ["uvicorn","app.main:app","--host", "0.0.0.0","--port","8000"]