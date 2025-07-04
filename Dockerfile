# Use lightweight official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (for many python packages we may face compatability issues)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libpq-dev \
        curl \
        procps \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .


# Set environment variable
ENV PYTHONPATH=/app:/app/src

# Expose ports for Airflow webserver, Flask, and MLflow
EXPOSE 5000 

# Default command
CMD ["python", "src/api/app.py"]



# # Set environment variable
# ENV AIRFLOW_HOME=/app/airflow 
# ENV PYTHONPATH=/app:/app/src

# # Expose ports for Airflow webserver, Flask, and MLflow
# EXPOSE 5000 8080 5001

# # Download and install wait-for-it/ it help other container to wait untill another execute
# RUN curl -o /usr/local/bin/wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh && \
#     chmod +x /usr/local/bin/wait-for-it.sh


# # Copy entrypoint script
# COPY entrypoint.sh /app/entrypoint.sh 
# RUN chmod +x /app/entrypoint.sh

# # Default command
# CMD ["/app/entrypoint.sh"]
