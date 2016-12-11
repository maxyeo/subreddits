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

### Levenshtein Distance
To train lambda_means algorithm:
`python classify.py --mode train --data output/unstopped_descriptions.txt --model-file output/unstopped_model.txt --algorithm lev`
