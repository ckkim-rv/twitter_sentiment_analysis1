import tweepy
from textblob import TextBlob
import preprocessor as p
import statistics

from keys import ckey,csecret

# I had a seprate keys file where I obtain the appropriate tokens for twitter API
authentication = tweepy.AppAuthHandler(ckey,csecret)
api = tweepy.API(authentication)

def get_tweets(keyword):
    tweets = []
    for tweet in tweepy.Cursor(api.search,q=keyword, tweet_mode='extended',result_type="recent", lang='en').items(50):
        tweets.append(p.clean(tweet.full_text))
    return tweets

def get_sentiment(tweets):
    sentiments = []
    for tweet in tweets:
        blob = TextBlob(tweet)
        sentiments.append(blob.sentiment.polarity)
    return sentiments

def scoring(keyword):
    tweets = get_tweets(keyword)
    scores = get_sentiment(tweets)
    for tweet,score in zip(tweets,scores):
        print(f"{tweet}: {score}")
    print("\n")
    avg = statistics.mean(scores)
    return avg

if __name__ == "__main__":
    max = -2
    best_word = ""
    for i in range(0, 10):
        keyword = input('Enter Keyword:')
        new_score = scoring(keyword)
        if new_score > max:
            max = new_score
            best_word = keyword
    print(f"{best_word} was the best tweet with the highest polarity score of {max}")
