FROM python:3.11

COPY . /app

# Install dependencies
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "tweet_streaming.py" ]