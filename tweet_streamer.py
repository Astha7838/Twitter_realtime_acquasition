from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import pika

class StreamTweets(StreamListener):

     def __init__(self,chan):
         self.channel = chan

     def on_data(self, tweet):
         try:
             self.channel.basic_publish(exchange='', routing_key='twitterqueue', body=tweet)
         except Exception as e:
             print("Error: %s" % e)

     def on_error(self,status_code):
         print(status_code)

     def on_exception(self, exception):
         print(exception)

if __name__ == "__main__":
        consumer_key = "ULItewxGYkR8ueTHxVpP7aVmE"
        consumer_secret = "tTYMqhqDs5hKQxvBfnz1KiUWaJKEq3PtXjniYvycdjmJteUYaQ"
        access_token = "1186025638622367745-Mb6BZ1vNn1dlOTgYs5MadKwO45M496"
        access_token_secret = "mntEfhh9o53i3m5jfSwRilCYOvGht42gby5eMOlSkzQ6r"

        auth = OAuthHandler(consumer_key,consumer_secret)
        auth.set_access_token(access_token,access_token_secret)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue='twitterqueue')

        tracklist = ["#climatechange", "#climatechangeisreal", "#actonclimate", "#globalwarming",
                     "#climatechangehoax", "#climatedeniers", "#climatechangeisfalse", "#globalwarminghoax",
                     "#climatechangenotreal","#greentweets", "#carbondioxide" ,"#CO2", "#carbonemissions",
                     "#greenhousegas","#greenhousegasses","#greenhousegasemissions",'#climatechange','#nature',
                     '#environment', '#climate', '#climatestrike', '#globalwarming', '#savetheplanet', '#sustainability',
                     '#gretathunberg', '#zerowaste', '#ecofriendly', '#climatecrisis', '#fridaysforfuture', '#earth',
                     '#climateaction', '#climatechangeisreal', '#plasticfree', '#gogreen', '#savetheearth', '#sustainable',
                     '#climatejustice', '#pollution', '#recycle', '#green', '#eco', '#climateemergency', '#extinctionrebellion',
                     '#vegan', '#saveourplanet']

        stream = Stream(auth,listener = StreamTweets(channel))
        print("Starting twitter stream..")
        stream.filter(track = tracklist, languages = ["en"])



