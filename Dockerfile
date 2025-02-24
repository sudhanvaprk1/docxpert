# Use an official Python runtime as a base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first (for better caching)
COPY deployments/requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK stopwords and tokenizer
RUN python -m nltk.downloader stopwords punkt punkt_tab

# Copy the rest of the application files
COPY . .

# Install Supervisor to manage multiple processes
RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

# Copy the Supervisor configuration file
COPY deployments/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose necessary ports
EXPOSE 5000 8501

# Start both Flask and Streamlit using Supervisor
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
