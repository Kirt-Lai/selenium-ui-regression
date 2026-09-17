# Use an official Python runtime as a parent image
# This image is based on Debian 12 (Bookworm)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Create and set permissions for the logs directory before any other operations
RUN mkdir -p logs && chmod -R 777 logs

# Install system dependencies
# - Note: libgconf-2-4 has been removed from the list as it is obsolete in
#   Debian Bookworm and no longer available.
# 安装 Git 和其他依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    wget \
    gnupg \
    curl \
    unzip \
    libglib2.0-0 \
    libnss3 \
    libfontconfig1 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libxtst6 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    xvfb \
    fonts-liberation \
    libgbm1 \
    libcups2 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
       > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver (auto matches Chrome version)
RUN CHROME_VERSION=$(google-chrome --version | awk '{print $3}') && \
    DRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
    wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/${DRIVER_VERSION}/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Install Allure CLI
RUN wget https://github.com/allure-framework/allure2/releases/download/2.13.8/allure-2.13.8.tgz && \
    tar -zxvf allure-2.13.8.tgz -C /opt && \
    ln -s /opt/allure-2.13.8/bin/allure /usr/local/bin/allure

# Create logs folder
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Copy the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# By default, run pytest when the container launches
CMD ["pytest"]
