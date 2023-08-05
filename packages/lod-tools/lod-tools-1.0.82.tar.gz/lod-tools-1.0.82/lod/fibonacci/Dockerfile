

# base this Image on python 3
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# this uses '-U -I --no-cache-dir --force-reinstall' for debugging purposes only,
# so that it always downloads the latest version of my dependencies whenever I change them.
# you probably don't need all of them, but some of these flags are bugged on some OS, and better safe than sorry.
RUN pip install -r requirements.txt -U -I --no-cache-dir --force-reinstall

# Run app.py when the container launches
CMD ["python", "app.py"]

