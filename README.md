# subreddits

Datasets reside in a folder called data which is gitignored because they are too large

# Lambda Means on Subreddit Activity

### Lambda Means on the Complete Data Set
To train lambda_means algorithm:
`python classify.py --mode train --data subreddits --model-file output/_activity_model.txt --algorithm lambda_means`

To run lambda_means algorithm:
`python classify.py --mode test --algorithm lambda_means --model-file output/subreddit_activity_model.txt --data output/subreddit_activity_test.txt --predictions-file output/subreddit_activity_predictions.txt`

To check the prediction accuracy:
`python compute_accuracy.py output/subreddit_activity_test.txt output/subreddit_activity_predictions.txt`

### Lambda Means on a Smaller Sample Data Set
To train lambda_means algorithm on a smaller sample:
`python classify.py --mode train --data output/subreddit_activity_train_sample.txt --model-file output/subreddit_activity_model.txt --algorithm lambda_means`

To run lambda_means algorithm on a smaller sample:
`python classify.py --mode test --algorithm lambda_means --model-file output/subreddit_activity_model.txt --data output/subreddit_activity_test_sample.txt --predictions-file output/subreddit_activity_predictions.txt`

To check the prediction accuracy on a smaller sample:
`python compute_accuracy.py output/subreddit_activity_test_sample.txt output/subreddit_activity_predictions.txt`

# Clustering on Descriptions

### Utilities for Parsing Descriptions
Original dataset can be found here: http://files.pushshift.io/reddit/subreddits/
There is a lot of extraneous information.  We only want to cluster the subreddits that were in the dataset above, so a utility to parse and extract only the relevant subreddits we use the following commands in a python shell
```python
>>> from parse_words import Descriptions
>>> descriptions = Descriptions()
>>> descriptions.subreddits_to_file()
```

to load the relevant subreddits from file into memory run
```python
>>> descriptions.load_subreddits_from_file()
```

we created a utility to only grab the descriptions from the large data set of the relevant subreddits and write to file, as well as a utility to read the file into memory
```python
>>> descriptions.descriptions_to_file()
>>> descriptions.load_descriptions_from_file()
```

we created a utility to parse through the markdown descriptions, turn them to html, then to plaintext, stripping extraeneous punctuation, and lowercasing all words and creating a corpus of words from all the words in the descriptions into a corpus
```python
>>> descriptions.corpus_to_file()
>>> descriptions.load_corpus_from_file()
```

finally we created a utility to calculate the word frequencies for each subreddit and create instances
```python
>>> descriptions.create_instances()`
```

### Levenshtein Distance
To make Levenshtein Distance operate better, we cleaned the descriptions by removing stop words, which can be done by using the utility 
```python
>>> descriptions.unstop_descriptions()`
>>> descriptions.load_unstopped_descriptions()`
```

To train lambda_means algorithm:
`python classify.py --mode train --data output/unstopped_descriptions.txt --model-file output/unstopped_model.txt --algorithm lev`
