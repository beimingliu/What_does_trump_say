import got
import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time
import sys


def tweet2df(username='barackobama', max_tweets=100):
    t = time.time()

    print('getting tweets...')
    tweetCriteria = got.manager.TweetCriteria().setUsername(username).setMaxTweets(max_tweets)
    tweet = got.manager.TweetManager.getTweets(tweetCriteria)
    print('Time to crawl tweets:', round(time.time() - t,1))

    df = pd.DataFrame()

    columns = ['text', 'date', 'favorites', 'retweets', 'hashtags', 'mentions', 'permalink', 'id']

    information = list([[] for i in range(len(columns))])

    information[0] = [tweet[i].text for i in range(len(tweet))]
    information[1] = [tweet[i].date for i in range(len(tweet))]
    information[2] = [tweet[i].favorites for i in range(len(tweet))]
    information[3] = [tweet[i].retweets for i in range(len(tweet))]
    information[4] = [tweet[i].hashtags for i in range(len(tweet))]
    information[5] = [tweet[i].mentions for i in range(len(tweet))]
    information[6] = [tweet[i].permalink for i in range(len(tweet))]
    information[7] = [tweet[i].id for i in range(len(tweet))]
    
    for i,c in enumerate(columns):
        # value can be a list, a Series, an array or a scalar   
        df.insert(loc=0, column=c, value=information[i])
        
    del information, tweet
    
    df = df[['text', 'date', 'favorites', 'retweets', 'hashtags', 'mentions', 'permalink', 'id']]
    analyzer = SentimentIntensityAnalyzer()
    df['score'] = [analyzer.polarity_scores(i)['compound'] for i in df['text']]
    
    # clean up
    df['mentions'] = df['mentions'].apply(lambda x: x.replace('@',''))
    df['mentions'] = df['mentions'].apply(lambda x: x.replace(' ',','))

    df['hashtags'] = df['hashtags'].apply(lambda x: x.replace('#',''))
    df['hashtags'] = df['hashtags'].apply(lambda x: x.replace(' ',','))

    df['mentions'] = df['mentions'].astype(str)
    df['hashtags'] = df['hashtags'].astype(str)
    
    df.to_excel('%s.xlsx' % username, index=False)
    print('Time to finsh the whole process:', round(time.time() - t,1))
    return df


if __name__ == "__main__":
    user = sys.argv[1]
    num_tweets = int(sys.argv[2])
    print(user, num_tweets)
    tweet2df(user, num_tweets)