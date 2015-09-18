"""
This script parses through input twitter data to count the number of times
each hashtag occurs. The top ten hashtags are then output to the screen.
"""

import sys
import json
import unicodedata

RM_PUNC_TBL = dict.fromkeys(i for i in xrange(sys.maxunicode) if
                            unicodedata.category(unichr(i)).startswith('P'))

def read_tweets(tweet_file_name):
    """
    Reads in the file of tweets and returns a list of tweets
    """
    tweet_file = open(tweet_file_name)
    tweet_data = []
    for line in tweet_file:
        tweet_data.append(json.loads(line))
    tweet_file.close()
    return tweet_data

def count_hashtags(tweet_data):
    """
    Counts all the occurences of each hashtag occuring in tweet_data and
    returns the result in a dictionary of the form {hashtag: count}.
    """
    hashtag_counts = {}
    for tweet in tweet_data:
        if 'entities' in tweet and tweet['entities'] is not None:
            hashtag_list = tweet['entities']['hashtags']
            if len(hashtag_list) > 0:
                for hashtag in tweet['entities']['hashtags']:
                    text = hashtag['text']
                    if text in hashtag_counts:
                        hashtag_counts[text] += 1
                    else:
                        hashtag_counts[text] = 1
    return hashtag_counts

def get_top_n(hashtag_counts, n):
    """
    Returns the top n hashtags in a list, sorted by count.
    """
    top_n = []
    for i, hashtag in enumerate(sorted(hashtag_counts, key = hashtag_counts.get, reverse = True)):
        if i >= n:
            return top_n
        top_n.append(hashtag)

def main():
    tweet_file_name = sys.argv[1]

    # Read in the tweet data file
    tweet_data = read_tweets(tweet_file_name)

    # Count the occurences of each hashtag
    hashtag_counts = count_hashtags(tweet_data)

    # Print the top ten hashtags and their count
    top_ten = get_top_n(hashtag_counts, 10)
    for hashtag in top_ten:
        print "{:30s} {:d}".format(hashtag.encode('utf-8'), hashtag_counts[hashtag])

if __name__ == '__main__':
    main()
