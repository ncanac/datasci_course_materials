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

def contained_in(lat, lng, bound_coords):
    """
    Returns true if (lat, lng) is contained within the polygon formed by the
    points in bound_coords.
    """
    bound_path = Path(np.array(bound_coords))
    return bound_path.contains_point((lat, lng))

def state_from_point(lat, lng, state_bounds):
    """
    Takes in a (latitude, longitude) point and returns the name of the state
    where this point is located.
    """
    for state, bound_coords in state_bounds.iteritems():
        if contained_in(lat, lng, bound_coords):
            return state, True
    return 'The Lost City of Atlantis', False

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

def calc_state_sents(tweet_data, scores, state_bounds):
    """
    Loops through the twitter data, and for each tweet for which a location
    can be determined, adds the sentiment score of the happiness total of that
    state and increments the total number of tweets.
    """
    # Initialize all states to have a sentiment score of 0
    state_sentiments = {}
    for state in STATE_ABBRV.keys():
        state_sentiments[state] = [0, 0]
    for tweet in tweet_data:
        if 'text' in tweet and 'coordinates' in tweet:
            if tweet['coordinates'] is not None:
                lat = tweet['coordinates']['coordinates'][1]
                lng = tweet['coordinates']['coordinates'][0]
                state, found = state_from_point(lat, lng, state_bounds)
                if found:
                    text = tweet['text']
                    state_sentiments[state][0] += calc_score(text, scores)
                    state_sentiments[state][1] += 1
    return state_sentiments

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

    # Read in state boundary information
    state_bounds = read_state_bounds()

    # Calculate the sentiment score for each state
    state_sentiments = calc_state_sents(tweet_data, scores, state_bounds)

    # Print the average sentiment score for each state
    total_count = 0
    print "State / Total sentiment score / Number of tweets / Average sentiment score"
    for state, data in state_sentiments.iteritems():
        total = data[0]
        count = data[1]
        avg = float(total)/count if count > 0 else 0
        total_count += count
        print "{:s} {:4d} {:3d} {:5.2f}".format(STATE_ABBRV[state],
                                                total, count, avg)
    print "Total tweets: ", total_count

if __name__ == '__main__':
    main()
