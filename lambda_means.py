from cs475_types import Predictor
import math

# LambdaMeans is a subclass of Predictor
class LambdaMeans(Predictor):
    def __init__(self, instances, subreddits, cluster_lambda, clustering_training_iterations):
        self.clustering_training_iterations = clustering_training_iterations
        self.subreddits = subreddits
        # Find mean of all instances and initialize the prototype vector to the mean of all instances
        # the size of prototype should be the maximum feature index
        self.maximum = 0
        for instance in instances:
            instanceMax = 0
            for key in instance._feature_vector.getFeatureVector().iterkeys():
                if key > instanceMax:
                    instanceMax = key
            if instanceMax > self.maximum:
                self.maximum = instanceMax

        # initialize prototype with 0s
        prototype = [0] * (self.maximum)

        for x in range(1, self.maximum + 1):
            for instance in instances:
                value = instance._feature_vector.getFeatureVector().get(x)
                if (value is not None):
                    prototype[x - 1] += value
            prototype[x - 1] /= len(instances)

        self.clambda = cluster_lambda
        # Set the value of lambda to the average distance from each training instance to the mean prototype vector
        distances = 0
        if (self.clambda == 0.0):
            for instance in instances:
                running_square_sum = 0
                for x in range(1, self.maximum + 1):
                    instanceVal = instance._feature_vector.getFeatureVector().get(x)
                    if instanceVal is None:
                        instanceVal = 0
                    prototypeVal = prototype[x - 1]

                    running_square_sum += math.pow(instanceVal - prototypeVal, 2)
                distances += math.sqrt(running_square_sum)

            # Find average of all instances
            self.clambda = distances / len(instances)

        self.num_clusters = 1
        self.prototypes = []
        self.prototypes.append(prototype)

    def train(self, instances):
        prototypeClusters = [[]]
        for x in range(1, self.clustering_training_iterations):
            counter = 0
            for instance in instances:
                counter += 1
                if counter % 100 == 0:
                    print(counter)
                # check which prototype the instance belongs to
                closestPrototypeIndex = -1
                closestPrototypeDistance = float("inf")
                curIndex = 0
                for prototype in self.prototypes:
                    running_square_sum = 0
                    for x in range(1, self.maximum + 1):
                        instanceVal = instance._feature_vector.getFeatureVector().get(x)
                        if instanceVal is None:
                            instanceVal = 0
                        prototypeVal = prototype[x - 1]

                        running_square_sum += math.pow(instanceVal - prototypeVal, 2)
                    distance = math.sqrt(running_square_sum)
                    if (distance < closestPrototypeDistance):
                        closestPrototypeDistance = distance
                        closestPrototypeIndex = curIndex
                    curIndex += 1

                # if instane is farther than lambda
                if (closestPrototypeDistance > self.clambda):
                    # create a new prototype
                    # initialize prototype with 0s
                    prototype = [0] * (self.maximum)

                    for x in range(1, self.maximum + 1):
                        value = instance._feature_vector.getFeatureVector().get(x)
                        if (value is not None):
                            prototype[x - 1] = value
                    self.prototypes.append(prototype)

                    # assign instance to cluster
                    prototypeClusters.append([])
                    prototypeClusters[-1].append(instance)
                else:
                    prototypeClusters[closestPrototypeIndex].append(instance)

            # maximization step
            curCluster = 0
            counter = 0
            for cluster in prototypeClusters:
                counter += 1
                print counter
                # if the cluster is empty make the prototype 0
                newprototype = [0] * (self.maximum)
                if (len(cluster) > 0):
                    for x in range(1, self.maximum + 1):
                        for instance in cluster:
                            value = instance._feature_vector.getFeatureVector().get(x)
                            if (value is not None):
                                newprototype[x - 1] += value
                        newprototype[x - 1] /= len(cluster)

                self.prototypes[curCluster] = newprototype
                curCluster += 1

    def predict(self, instance):
        closestPrototypeIndex = -1
        closestPrototypeDistance = float("inf")
        curIndex = 0
        for prototype in self.prototypes:
            running_square_sum = 0
            for x in range(1, self.maximum + 1):
                instanceVal = instance._feature_vector.getFeatureVector().get(x)
                if instanceVal is None:
                    instanceVal = 0
                prototypeVal = prototype[x - 1]

                running_square_sum += math.pow(instanceVal - prototypeVal, 2)
            distance = math.sqrt(running_square_sum)
            if (distance < closestPrototypeDistance):
                closestPrototypeDistance = distance
                closestPrototypeIndex = curIndex
            curIndex += 1

        # The closest prototype is stored in closestPrototypeIndex
        closestPrototype = self.prototypes[closestPrototypeIndex]
        highestFeatureValue = closestPrototype[0]
        highestFeatureIndex = 0
        counter = 0
        for feature in closestPrototype:
            if feature >= highestFeatureValue:
                highestFeatureValue = feature
                highestFeatureIndex = counter
                counter += 1

        # Now find the subreddit corresponding to highestFeatureIndex
        return self.subreddits[highestFeatureIndex]
