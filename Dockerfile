# Use Puppeteer's Chromium-enabled base image
FROM ghcr.io/puppeteer/puppeteer:latest

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

# Expose Flask default port
EXPOSE 5000

# Run app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
