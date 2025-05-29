FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variable
ENV AIRFLOW_HOME=/app/airflow 
ENV PYTHONPATH=/app:/app/src

# Install wait-for-it script
# it install i needed libries and update them and skip installation and updatation for not important libries and 
# and next commands wait for the to start all images in needed flow and next one clear the catch to reduce the size

# Install curl first
RUN apt-get update && apt-get install -y curl

# Download and install wait-for-it
RUN curl -o /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
    chmod +x /usr/local/bin/wait-for-it.sh


EXPOSE 5000 8080

#Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh 
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]


