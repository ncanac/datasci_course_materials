import sys
import json
import unicodedata

RM_PUNC_TBL = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))

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

def calc_term_freq(tweet_data):
    """
    Calculates the frequency of each term occuring in the twitter output file.
    Frequency is calculated as:
    [# of occurrences of the term]/[# of occurrences of all terms]
    """
    terms = []
    term_counts = []
    total_terms = 0
    for tweet in tweet_data:
        if 'text' in tweet:
            text = tweet['text'].translate(RM_PUNC_TBL).lower()
            for term in text.split():
                if term in terms:
                    idx = terms.index(term)
                    term_counts[idx] += 1
                else: # not in terms so add
                    terms.append(term)
                    term_counts.append(1)
                total_terms += 1
    term_freq = {}
    for term, count in zip(terms, term_counts):
        term_freq[term] = float(count)/total_terms
    return term_freq

def main():
    tweet_file_name = sys.argv[1]

    # Read in the tweet data file
    tweet_data = read_tweets(tweet_file_name)

    # Calculate the term frequency for each term in the twitter data
    term_freq = calc_term_freq(tweet_data)

    # Write results to file
    outfile = open('term_frequencies.txt', 'w')
    for term, freq in term_freq.iteritems():
        outfile.write(term.encode('utf-8') + "\t" + str(freq) + "\n")
    outfile.close()

if __name__ == '__main__':
    main()
