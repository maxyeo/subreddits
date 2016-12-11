from cs475_types import Predictor
import math

# LambdaMeans is a subclass of Predictor
class LambdaMeans(Predictor):
    def __init__(self, instances, subreddits, cluster_lambda, clustering_training_iterations):
        self.clustering_training_iterations = clustering_training_iterations
        self.subreddits = subreddits
        # Find mean of all instances and initialize the prototype vector to the mean of all instances

        # the size of prototype should be the maximum feature index
        self.maximum = self.find_max_index(instances)

        # initialize prototype with 0s
        prototype = [0] * (self.maximum)

        for x in range(1, self.maximum + 1):
            for instance in instances:
                value = instance._feature_vector.getFeatureVector().get(x)
                if value is not None:
                    prototype[x - 1] += value
            prototype[x - 1] /= len(instances)

        self.clambda = cluster_lambda
        # Set the value of lambda to the average distance from each training instance to the mean prototype vector
        distances = 0
        if self.clambda == 0.0:
            for instance in instances:
                running_square_sum = 0
                for x in range(1, self.maximum + 1):
                    instanceVal = instance._feature_vector.getFeatureVector().get(x)
                    if instanceVal is None:
                        instanceVal = 0
                    prototypeVal = prototype[x - 1]

                    running_square_sum += math.pow(instanceVal - prototypeVal, 2)
                distances += running_square_sum

            # Find average of all instances
            self.clambda = distances / len(instances)

        self.num_clusters = 1
        self.prototypes = [prototype]

    def train(self, instances):
        for x in range(1, self.clustering_training_iterations + 1):
            print x
            prototypeClusters = [] # A list of lists
            for prototype in self.prototypes:
                prototypeClusters.append([])
            for instance in instances:
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
                    prototypeClusters.append([instance])
                else:
                    prototypeClusters[closestPrototypeIndex].append(instance)

            print x
            # maximization step
            curCluster = 0
            for cluster in prototypeClusters:
                # if the cluster is empty make the prototype 0
                newprototype = [0] * (self.maximum)
                if len(cluster) > 0:
                    for x in range(1, self.maximum + 1):
                        for instance in cluster:
                            value = instance._feature_vector.getFeatureVector().get(x)
                            if value is not None:
                                newprototype[x - 1] += value
                        newprototype[x - 1] /= len(cluster)

                self.prototypes[curCluster] = newprototype
                curCluster += 1
            print x

    def predict(self, instance):
        closestPrototypeIndex = self.getClosestPrototypeIndexAndDistance(instance)[0]
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
        if int(str(instance._label)) % 100 == 0:
            print str(instance._label)
        return self.subreddits[highestFeatureIndex]

    def find_max_index(self, instances):
        maximum = -1
        for instance in instances:
            instanceMax = 0
            for key in instance._feature_vector.getFeatureVector().iterkeys():
                if key > instanceMax:
                    instanceMax = key
            if instanceMax > maximum:
                maximum = instanceMax

        return maximum

    def getClosestPrototypeIndexAndDistance(self, instance):
        closestPrototypeIndex = -1
        closestPrototypeDistance = float("inf")
        curIndex = 0
        for prototype in self.prototypes:
            distance = self.get_distance(prototype, instance._feature_vector.getFeatureVector())

            if (distance < closestPrototypeDistance):
                closestPrototypeDistance = distance
                closestPrototypeIndex = curIndex
            curIndex += 1

        return (closestPrototypeIndex, closestPrototypeDistance)

    def create_prototype(self, instance_feature_vector):
        # initialize prototype with 0s
        prototype = [0] * self.maximum

        for x in range(1, self.maximum + 1):
            value = instance_feature_vector.get(x)
            if value is not None:
                prototype[x - 1] = value

        return prototype

    def get_distance(self, prototype, instance_feature_vector):
        running_square_sum = 0
        for x in range(0, self.maximum):
            instanceVal = instance_feature_vector.get(x + 1)
            if instanceVal is None:
                instanceVal = 0
            prototypeVal = prototype[x]

            running_square_sum += math.pow(instanceVal - prototypeVal, 2)

        return running_square_sum
