import os
import sqlite3

import random
import tweepy
from geopy.exc import GeocoderTimedOut
from tweepy import Stream
from tweepy import OAuthHandler
from geopy.geocoders import Nominatim
from instance import config
from config import LOG_DIR
from logger import setup_logger
from medmap.meta import DISEASES

geolocator = Nominatim(user_agent="Pauva")

stream_logger = setup_logger(name=__name__, log_file=os.path.join(LOG_DIR, 'streaming_log'), level="DEBUG")


class StreamListener(tweepy.streaming.StreamListener):
    def __init__(self, db_conn):
        super(StreamListener, self).__init__()
        self.conn = db_conn
        self.num_tweets = 0

    def on_status(self, status):
        try:
            status_text = str(status.text).encode('ascii', 'ignore')
            status_timestamp = str(status.created_at)
            temp_str = status_text.decode('ascii').split(" ")
            status_disease = ""
            for item in temp_str:
                if item.lower() in DISEASES:
                    status_disease = item.lower()
                    break
            if status.coordinates is None:
                user_loc = status.user.location
                if user_loc is None:
                    return
                location = geolocator.geocode(user_loc)
                if location is None:
                    return
                status_geo_lat, status_geo_long = str(location.latitude), str(location.longitude)
            else:
                status_geo_lat, status_geo_long = status.coordinates
            self.conn.execute("INSERT INTO APP (STATUS, TIMESTAMP, GEO_LAT, GEO_LONG, DISEASE) VALUES (?, ?, ?, ?, ?)",
                              (status_text, status_timestamp, status_geo_lat, status_geo_long, status_disease))
            self.conn.commit()
            self.num_tweets += 1
            if random.random() < 0.2:
                stream_logger.info("Number of relevant tweets increased by {0}".format(self.num_tweets))
                self.num_tweets = 0
        except UnicodeEncodeError:
            pass
        except GeocoderTimedOut:
            pass
        except Exception:
            stream_logger.exception("Unknown Exception.")

    def on_error(self, status_code):
        if status_code == 420:
            return False


def start_streaming(db_conn):
    """

    :param db_conn: Database connection object.
    :return:
    """
    ckey = config.TWITTER_KEYS['CONSUMER_KEY']
    csecret = config.TWITTER_KEYS['CONSUMER_SECRET']
    atoken = config.TWITTER_KEYS['ACCESS_TOKEN']
    asecret = config.TWITTER_KEYS['ACCESS_SECRET']

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    stream_logger.debug("Streaming started")
    twitter_stream = Stream(auth, StreamListener(db_conn))
    twitter_stream.filter(languages=["en"], track=DISEASES, async=True)
