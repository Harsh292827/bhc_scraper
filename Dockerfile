FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget unzip curl gnupg \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome manually
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && mv chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver

# Copy app code
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000

# Run the Flask app via Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
