import pika
import json
import csv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import re
import os


def process_tweet(data):
    try:
            id = data["id"]
            text = data["text"].strip()
            created_at = data["created_at"]
            username = data["user"]["name"]
            user_id = data["user"]["id"]
            user_location = data["user"]["location"]
            quoted_full_text = None
            retweet_full_text = None
            if 'quoted_status' in data and 'extended_tweet' in data['quoted_status'].keys():
                     quoted_full_text = data['quoted_status']['extended_tweet']['full_text'].strip()
            elif 'retweeted_status' in data and 'extended_tweet' in data['retweeted_status'].keys():
                     retweet_full_text = data['retweeted_status']['extended_tweet']['full_text'].strip()
            ps = PorterStemmer()
            stop_words = set(stopwords.words('english'))
            if quoted_full_text is None and retweet_full_text is None:
                     httpremoved = re.sub(r"http\S+", "",text)
                     no_special_charac = re.sub('[^A-Za-z0-9\s]+', '', httpremoved)
                     words = word_tokenize(no_special_charac)
                     not_common_words = [w for w in words if not w in stop_words]
                     stemmed_words = [ps.stem(w) for w in not_common_words]
                     row = [id,created_at,username,user_id,user_location,text,stemmed_words]
            elif quoted_full_text is None:
                     httpremoved = re.sub(r"http\S+", "", retweet_full_text)
                     no_special_charac = re.sub('[^A-Za-z0-9\s]+', '', httpremoved)
                     words = word_tokenize(no_special_charac)
                     not_common_words = [w for w in words if not w in stop_words]
                     stemmed_words = [ps.stem(w) for w in not_common_words]
                     row = [id,created_at,username,user_id,user_location,retweet_full_text,stemmed_words]
            elif retweet_full_text is None:
                     httpremoved = re.sub(r"http\S+", "", quoted_full_text)
                     no_special_charac = re.sub('[^A-Za-z0-9\s]+', '', httpremoved)
                     words = word_tokenize(no_special_charac)
                     not_common_words = [w for w in words if not w in stop_words]
                     stemmed_words = [ps.stem(w) for w in not_common_words]
                     row = [id, created_at, username, user_id, user_location, quoted_full_text,stemmed_words]
            writer.writerow(row)
    except Exception as e:
            file.close()
            print("Error: %s" %e)

def callback(ch, method, properties, body):
    data = json.loads(body)
    process_tweet(data)


if __name__ == "__main__":
    header = ['tweet_id', 'created_at', 'username', 'user_id', 'user_location', 'text','stemmed_words']
    if not os.path.isfile('/home/tweet/tweet_data.csv'):
         file =  open("/home/tweet/tweet_data.csv", "a",encoding="utf-8")
         writer = csv.writer(file,delimiter=',')
         writer.writerow(header)
    else:
        file = open("/home/tweet/tweet_data.csv", "a", encoding="utf-8")
        writer = csv.writer(file, delimiter=',')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='twitterqueue')
    channel.basic_consume(
    queue='twitterqueue', on_message_callback=callback, auto_ack=True)
    print('Waiting for Tweets..')

    channel.start_consuming()
