import sys
import json
import string

def lines(fp):
    print str(len(fp.readlines()))

def calc_score(text, scores):
    """
    Calculates the sentiment score of an input string text.
    """
    score = 0
    for word in text.split():
        # Convert characters to lowercase and strip punctuation
        transdict = string.maketrans(string.punctuation, " "*len(string.punctuation))
        word = word.translate(transdict)
        score += scores[word.lower()] if word.lower() in scores else 0
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

    #lines(sent_file)
    #lines(tweet_file)

    # initialize empty dictionary for words and their corresponding sentiment scores
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

    print tweet_data[5]['text']
    print tweet_data[7]['text']
    print tweet_data[13]['text']

if __name__ == '__main__':
    main()
