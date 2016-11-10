import os
import pandas
import re

def clean_tweets(file_name):
    try:
        tweetfile = pandas.read_csv(file_name)
        tweetfile = tweetfile.fillna('')
    except IOError:
        print("Error")
        return

    tweetfile['Cleaned_tweet'] = [re.sub(r'http\S+|#\S+|@\S+|', '', w) for w in tweetfile['text']]
    tweetfile['Cleaned_tweet'] = [re.sub(r'\d+', '', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [w.lower() for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub('^rt', '', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub('&amp', '', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub('[$(&?!/;:]', '.', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub('\'s|,|-', ' ', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [s.strip() for s in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub(r'(.)\1+', r'\1\1', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub(r'[^\w.]', ' ', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [s.strip() for s in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub(r'\.(?=\.)|\G(?!^)\.', '', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub(r'(.)\1+[ ]', r'\1 ', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub(r'(.)\1+$', r'\1', w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub(r'[\.]',' ',w) for w in tweetfile['Cleaned_tweet']]
    tweetfile['Cleaned_tweet'] = [re.sub(' +', ' ', w) for w in tweetfile['Cleaned_tweet']]
    os.chdir('./../cleaned_data')
    tweetfile.to_csv(file_name[:-11] + '_cleaned.csv')
    pass

os.chdir('./data')
filenames = os.listdir(os.getcwd())
t = len(filenames)
i = 0

if filenames[0].endswith('_tweets.csv'):
    i += 1
    clean_tweets(filenames[0])
    print "Cleaned : " + "(" + str(i) + "/" + str(t) +") " + filenames[0]
else:
    print "Invalid File."

for f in filenames:
    i += 1
    os.chdir('./../data')
    if f.endswith('_tweets.csv'):
        clean_tweets(f)
        print "Cleaned : " + "(" + str(i) + "/" + str(t) +") " + f
    else:
        print "Invalid File."
