#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print 'usage: %s data predictions' % sys.argv[0]
    sys.exit()

data_file = sys.argv[1]
predictions_file = sys.argv[2]

data = open(data_file)
predictions = open(predictions_file)

# Load the real labels.
true_labels = []
for line in data:
    split_line = line.split(",")
    split_line.pop(0)
    subreddits = []
    for subreddit in split_line:
        # sometimes there is an extraneous "\n"
        if "\n" in subreddit:
            subreddit = subreddit.replace("\n", "")
        if subreddit not in subreddits:
            subreddits.append(subreddit)
    true_labels.append(subreddits)

predicted_labels = []
for line in predictions:
    if "\n" in line:
        line = line.replace("\n", "")
    predicted_labels.append(line)

data.close()
predictions.close()

if len(predicted_labels) != len(true_labels):
    print 'Number of lines in two files do not match.'
    sys.exit()

match = 0
total = len(predicted_labels)

for ii in range(len(predicted_labels)):
    if predicted_labels[ii] in true_labels[ii]:
        match += 1

print 'Accuracy: %f (%d/%d)' % ((float(match)/float(total)), match, total)
