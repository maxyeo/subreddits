from cs475_types import Predictor
import math
import numpy as np

# LambdaMeans is a subclass of Predictor
class LambdaMeans(Predictor):
    def __init__(self, instances, subreddits, cluster_lambda, clustering_training_iterations):
        self.clustering_training_iterations = clustering_training_iterations
        self.subreddits = subreddits
        # Find mean of all instances and initialize the prototype vector to the mean of all instances

        # the size of prototype should be the maximum feature index
        self.maximum = self.find_max_index(instances)

        prototype_array = []
        for instance in instances:
            prototype_array.append(self.create_prototype(instance._feature_vector.getFeatureVector()))

        prototype = np.mean(np.array(prototype_array), axis=0)


        self.clambda = cluster_lambda
        # Set the value of lambda to the average distance from each training instance to the mean prototype vector
        distances = 0
        if self.clambda == 0.0:
            for instance in instances:
                distances += self.get_distance(prototype, instance._feature_vector.getFeatureVector())

            # Find average of all instances
            self.clambda = distances / len(instances)

        self.clambda = self.clambda / 100.0

        self.num_clusters = 1
        self.prototypes = [prototype]

    def train(self, instances):
        for x in range(1, self.clustering_training_iterations + 1):
            #print x
            prototypeClusters = [] # A list of lists
            for prototype in self.prototypes:
                prototypeClusters.append([])
            counter = 0
            for instance in instances:
                counter += 1
                if counter % 100 == 0:
                    print counter
                # check which prototype the instance belongs to
                closestPrototype = self.getClosestPrototypeIndexAndDistance(instance)
                closestPrototypeIndex = closestPrototype[0]
                closestPrototypeDistance = closestPrototype[1]

                # if instance is farther than lambda
                if closestPrototypeDistance > self.clambda:
                    # create a new prototype
                    prototype = self.create_prototype(instance._feature_vector.getFeatureVector())
                    self.prototypes.append(prototype)

                    # assign instance to new prototype
                    prototypeClusters.append([self.create_prototype(instance._feature_vector.getFeatureVector())])
                else:
                    prototypeClusters[closestPrototypeIndex].append(self.create_prototype(instance._feature_vector.getFeatureVector()))

            # maximization step
            curCluster = 0
            for cluster in prototypeClusters:
                # if the cluster is empty make the prototype 0
                if len(cluster) == 0:
                    newprototype = [0] * self.maximum
                else:
                    newprototype = np.mean(np.array(cluster), axis=0)

                self.prototypes[curCluster] = newprototype
                curCluster += 1

    def predict(self, instance):
        closestPrototypeIndex = self.getClosestPrototypeIndexAndDistance(instance)[0]
        closestPrototype = self.prototypes[closestPrototypeIndex]

        highestFeatureIndex = 0
        highestFeatureValue = max(closestPrototype)
        if highestFeatureValue != 0:
            highestFeatureIndex = np.where(closestPrototype == highestFeatureValue)[0][0]

        # Now find the subreddit corresponding to highestFeatureIndex
        if int(str(instance._label)) % 100 == 0:
            print str(instance._label)
        return self.subreddits[highestFeatureIndex]

    def find_max_index(self, instances):
        global_max = -1
        for instance in instances:
            local_max = max(instance._feature_vector.getFeatureVector().iterkeys())
            if local_max > global_max:
                global_max = local_max

        return global_max

    def getClosestPrototypeIndexAndDistance(self, instance):
        closestPrototypeIndex = -1
        closestPrototypeDistance = float("inf")
        curIndex = 0
        for prototype in self.prototypes:
            distance = self.get_distance(prototype, instance._feature_vector.getFeatureVector())

            if distance < closestPrototypeDistance:
                closestPrototypeDistance = distance
                closestPrototypeIndex = curIndex
            curIndex += 1

        return (closestPrototypeIndex, closestPrototypeDistance)

    def create_prototype(self, instance_feature_vector):
        # initialize prototype with 0s
        prototype = [0] * self.maximum

        for key, value in instance_feature_vector.iteritems():
            prototype[key - 1] = value

        return prototype

    def get_distance(self, prototype, instance_feature_vector):
        a = np.array(prototype)
        b = np.array(self.create_prototype(instance_feature_vector))

        return math.pow(np.linalg.norm(a-b), 2)
