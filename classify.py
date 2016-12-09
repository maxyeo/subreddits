import os
import argparse
import sys
import pickle

from cs475_types import ClassificationLabel, FeatureVector, Instance, Predictor
from parse_words import Descriptions
from lambda_means import LambdaMeans

def load_data(filename):
    subreddits = []
    counter = 0
    instances = []

    descriptions = Descriptions()
    # descriptions.load_subreddits_from_file()
    descriptions.load_descriptions_from_file()
    descriptions.load_corpus_from_file()
    descriptions.create_instances()

    return instances

def load_more_data(filename):
    subreddits = []
    counter = 0
    instances = []

    # figure out what all the possible Subreddits are
    with open(filename) as reader:
        for line in reader:
            if len(line.strip()) == 0:
                continue

            split_line = line.split(",")
            split_line.pop(0)
            for subreddit in split_line:
                # sometimes there is an extraneous "\n"
                if "\n" in subreddit:
                    subreddit = subreddit.replace("\n", "")
                if subreddit not in subreddits:
                    subreddits.append(subreddit)

            counter += 1
            if counter % 10000 == 0:
                print(counter)

    # each Subreddit's index in the FeatureVector is it's position in self.subreddits[]
    # iterate through file again
    counter = 0
    with open(filename) as reader:
        for line in reader:
            if len(line.strip()) == 0:
                continue

            split_line = line.split(",")
            label = ClassificationLabel(split_line[0])
            split_line.pop(0)

            feature_vector = FeatureVector()

            for subreddit in split_line:
                # sometimes there is an extraneous "\n"
                if "\n" in subreddit:
                    subreddit = subreddit.replace("\n", "")
                feature = subreddits.index(subreddit)
                feature_vector.add(feature, 1)

            instance = Instance(feature_vector, label)
            instances.append(instance)

            counter += 1
            if counter % 10000 == 0:
                print(counter)

    # for i in instances:
    #     print i._label
    #     print i._feature_vector.feature_vector
    return instances


def get_args():
    parser = argparse.ArgumentParser(description="This is the main test harness for your algorithms.")

    parser.add_argument("--data", type=str, required=True, help="The data to use for training or testing.")
    parser.add_argument("--mode", type=str, required=True, choices=["train", "test"],
                        help="Operating mode: train or test.")
    parser.add_argument("--model-file", type=str, required=True,
                        help="The name of the model file to create/load.")
    parser.add_argument("--predictions-file", type=str, help="The predictions file to create.")
    parser.add_argument("--algorithm", type=str, help="The name of the algorithm for training.")

    parser.add_argument("--cluster-lambda", type=float, help="The value of lambda in lambda-means.", default=0.0)
    parser.add_argument("--clustering-training-iterations", type=int, help="The number of clustering iterations.", default=10)

    args = parser.parse_args()
    check_args(args)

    return args


def check_args(args):
    if args.mode.lower() == "train":
        if args.algorithm is None:
            raise Exception("--algorithm should be specified in mode \"train\"")
    else:
        if args.predictions_file is None:
            raise Exception("--algorithm should be specified in mode \"test\"")
        if not os.path.exists(args.model_file):
            raise Exception("model file specified by --model-file does not exist.")


def train(instances, algorithm, cluster_lambda, clustering_training_iterations):
    if algorithm == "lambda_means":
        lambda_means = LambdaMeans(instances, self.subreddits, cluster_lambda, clustering_training_iterations)
        lambda_means.train(instances)
        return lambda_means


def write_predictions(predictor, instances, predictions_file):
    try:
        with open(predictions_file, 'w') as writer:
            for instance in instances:
                label = predictor.predict(instance)

                writer.write(str(label))
                writer.write('\n')
    except IOError:
        raise Exception("Exception while opening/writing file for writing predicted labels: " + predictions_file)


def main():
    args = get_args()

    if args.mode.lower() == "train":
        # Load the training data.
        if "subreddits_small.txt" in args.data or "subreddits.txt" in args.data:
            instances = load_data(args.data)
            # Train the model.
            predictor = train(instances, args.algorithm, args.cluster_lambda, args.clustering_training_iterations)
        else:
            instances_and_subreddits = load_more_data(args.data)
            instances = instances_and_subreddits[0]
            subreddits = instances_and_subreddits[1]
            # Train the model.
            predictor = train(instances, subreddits, args.algorithm, args.cluster_lambda, args.clustering_training_iterations)

        try:
            with open(args.model_file, 'wb') as writer:
                pickle.dump(predictor, writer)
        except IOError:
            raise Exception("Exception while writing to the model file.")
        except pickle.PickleError:
            raise Exception("Exception while dumping pickle.")

    elif args.mode.lower() == "test":
        # Load the test data.
        instances = load_data(args.data)

        predictor = None
        # Load the model.
        try:
            with open(args.model_file, 'rb') as reader:
                predictor = pickle.load(reader)
        except IOError:
            raise Exception("Exception while reading the model file.")
        except pickle.PickleError:
            raise Exception("Exception while loading pickle.")

        write_predictions(predictor, instances, args.predictions_file)
    else:
        raise Exception("Unrecognized mode.")

if __name__ == "__main__":
    main()
