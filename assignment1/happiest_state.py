"""
This script calculates the average sentiment scores for tweets coming from each
state in order to determine the "happiest" state.
Notes:
-Use 'coordinates', 'place', or 'user' keywords to find location
-Can use 'lang' keyword to find only English tweets
"""

import sys
import json
import unicodedata
import numpy as np
import xml.etree.ElementTree as ET
from matplotlib.path import Path

STATE_ABBRV = { 'Alaska': 'AK',
                'Alabama': 'AL',
                'Arkansas': 'AR',
                'Arizona': 'AZ',
                'California': 'CA',
                'Colorado': 'CO',
                'Connecticut': 'CT',
                'Delaware': 'DE',
                'Florida': 'FL',
                'Georgia': 'GA',
                'Hawaii': 'HI',
                'Iowa': 'IA',
                'Idaho': 'ID',
                'Illinois': 'IL',
                'Indiana': 'IN',
                'Kansas': 'KS',
                'Kentucky': 'KY',
                'Louisiana': 'LA',
                'Massachusetts': 'MA',
                'Maryland': 'MD',
                'Maine': 'ME',
                'Michigan': 'MI',
                'Minnesota': 'MN',
                'Missouri': 'MO',
                'Mississippi': 'MS',
                'Montana': 'MT',
                'North Carolina': 'NC',
                'North Dakota': 'ND',
                'Nebraska': 'NE',
                'New Hampshire': 'NH',
                'New Jersey': 'NJ',
                'New Mexico': 'NM',
                'Nevada': 'NV',
                'New York': 'NY',
                'Ohio': 'OH',
                'Oklahoma': 'OK',
                'Oregon': 'OR',
                'Pennsylvania': 'PA',
                'Rhode Island': 'RI',
                'South Carolina': 'SC',
                'South Dakota': 'SD',
                'Tennessee': 'TN',
                'Texas': 'TX',
                'Utah': 'UT',
                'Virginia': 'VA',
                'Vermont': 'VT',
                'Washington': 'WA',
                'Wisconsin': 'WI',
                'West Virginia': 'WV',
                'Wyoming': 'WY' }

RM_PUNC_TBL = dict.fromkeys(i for i in xrange(sys.maxunicode) if
                            unicodedata.category(unichr(i)).startswith('P'))

def read_state_bounds():
    """
    Reads in the coordinates for the boundary of each state provided in the xml
    file state_boundaries.xml and returns a dictionary of state names and their
    cooresponding boundaries as a list of latitude and longitude pairs.
    """
    tree = ET.parse('state_boundaries.xml')
    states = tree.getroot()
    state_bounds = {}
    count = 0
    for state in states:
        coords = []
        for point in state:
            coords.append([point.attrib['lat'], point.attrib['lng']])
        name = state.attrib['name']
        state_bounds[name] = coords
    return state_bounds

def calc_score(text, scores):
    """
    Calculates the sentiment score of an input string text.
    """
    score = 0
    for word in text.split():
        # Convert characters to lowercase and strip punctuation
        word = word.translate(RM_PUNC_TBL)
        word = word.lower()
        score += scores[word] if word in scores else 0
    return score

def assign_sent(tweet_data, scores):
    """
    For each tweet, prints the sentiment score for each tweet to a file.
    """
    outfile = open('tweet_sentiment_scores.txt', 'w')
    for tweet in tweet_data:
        if 'text' in tweet:
            outfile.write(str(calc_score(tweet['text'], scores)) + "\n")
        else:
            outfile.write(str(0) + "\n")
    outfile.close()

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    # initialize empty dictionary for terms and their sentiment scores
    scores = {}
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    sent_file.close()

    # read in the tweet_file
    tweet_data = []
    for line in tweet_file:
        tweet_data.append(json.loads(line))
    tweet_file.close()

    assign_sent(tweet_data, scores)

    # Read in state boundary information
    state_bounds = read_state_bounds()

if __name__ == '__main__':
    main()
