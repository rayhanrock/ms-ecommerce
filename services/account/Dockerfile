FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Clean up the package cache
RUN rm -rf /var/cache/apk/*

LABEL maintainer="Rayhan Billah <rayhanbillah@hotmail.com>"
LABEL description="Docker image for account service"


EXPOSE 80

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

# Run the FastAPI application
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]



