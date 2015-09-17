import sys
import json
import unicodedata

RM_PUNC_TBL = dict.fromkeys(i for i in xrange(sys.maxunicode) if unicodedata.category(unichr(i)).startswith('P'))

def init_scores(sent_file_name):
    """
    Initializes dictionary of words and their sentiment scores from an input
    file.
    """
    sent_file = open(sent_file_name)
    scores = {}
    for line in sent_file:
        term, score = line.split("\t")
        scores[term] = int(score)
    sent_file.close()
    return scores

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

def assign_new_scores(tweet_data, scores):
    """
    Assign sentiment scores for words that aren't contained in scores by
    effectively averaging the sentiment scores for all the tweets that contain
    the word.
    """
    new_words = []
    word_totals = []
    word_counts = []
    for tweet in tweet_data:
        if 'text' in tweet:
            text = tweet['text'].translate(RM_PUNC_TBL).lower()
            score = calc_score(text, scores)
            for word in text.split():
                if word not in scores:
                    if word not in new_words:
                        new_words.append(word)
                        word_totals.append(score)
                        word_counts.append(1)
                    else: # already in new_words
                        idx = new_words.index(word)
                        word_totals[idx] += score
                        word_counts[idx] += 1
    new_scores = {}
    for word, total, count in zip(new_words, word_totals, word_counts):
        new_scores[word] = int(round(total/count))
    return new_scores

def main():
    sent_file_name = sys.argv[1]
    tweet_file_name = sys.argv[2]

    # Initialize dictionary of known scores
    scores = init_scores(sent_file_name)

    # Read in the tweet data file
    tweet_data = read_tweets(tweet_file_name)

    # Create a new dictionary for words that do not already have a score
    new_scores = assign_new_scores(tweet_data, scores)

    # Write results to file
    outfile = open('new_word_sentiment_scores.txt', 'w')
    for word, score in new_scores.iteritems():
        outfile.write(word.encode('utf-8') + "\t" + str(score) + "\n")
    outfile.close()

    # Output results to stdout
    #for word, score in new_scores.iteritems():
    #    print word.encode('utf-8'), " ", score

if __name__ == '__main__':
    main()
