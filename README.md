# subreddits

Datasets reside in a folder called data which is gitignored because they are too large

To train lambda_means algorithm:
python classify.py --mode train --data output/subreddit_activity_train.txt --model-file output/subreddit_activity_model.txt --algorithm lambda_means

To train lambda_means algorithm on a smaller sample:
python classify.py --mode train --data output/subreddit_activity_train_sample.txt --model-file output/subreddit_activity_model.txt --algorithm lambda_means

To run lambda_means algorithm:
python classify.py --mode test --algorithm lambda_means --model-file output/subreddit_activity_model.txt --data output/subreddit_activity_test.txt --predictions-file output/subreddit_activity_predictions.txt
