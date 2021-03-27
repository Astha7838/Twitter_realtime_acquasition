FROM python

RUN apt-get update && \
    apt-get install -y rabbitmq-server &&\
    apt install -y python3-pip && \
    pip3 install tweepy  && \ 
    pip3 install pika  && \
    pip3 install nltk

RUN python3 -m nltk.downloader -d /usr/local/share/nltk_data stopwords punkt
RUN mkdir -p /home/application

COPY tweet_processor.py /home/application
COPY tweet_streamer.py /home/application

RUN mkdir -p /home/tweet

VOLUME ["/home/tweet"]

CMD service rabbitmq-server start; exec python3 /home/application/tweet_processor.py & exec python3 /home/application/tweet_streamer.py


