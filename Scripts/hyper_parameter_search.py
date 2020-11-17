# Dependencies
import time
import pickle
import random
import statistics
from Scripts.utils import training, testing


# HyperParameters: k, reduction_percentage, classifier
def choose_classifier(data, k, reduction_percentage):
    classifiers = ['10-nearest-neighbors',
                   'nearest-centroid-mean',
                   'nearest-centroid-median',
                   'logistic-regression',
                   'linear-svm',
                   'quadratic-svm',
                   'cubic-svm',
                   'sgd',
                   'decision-tree',
                   'random-forest',
                   'adaboost',
                   'gaussian-naive-bayes',
                   'lda',
                   'qda',
                   'multilayer-perceptron']

    # 10-fold cross validation
    accuracies = {}
    running_time = {}
    index = 0
    step = int(len(data) / 10)
    random.shuffle(data)

    for classifier in classifiers:
        accuracies[classifier] = []
        running_time[classifier] = []

    for i in range(1):
        print("training model #" + str(i + 1))
        train = data[:index] + data[index + step:]
        test = data[index:index + step]
        index = index + step

        for classifier in classifiers:
            start = time.time()
            pipeline = training(train, k, classifier, reduction_percentage)
            accuracy = testing(test, k, pipeline)
            stop = time.time()
            accuracies[classifier].append(accuracy)
            running_time[classifier].append((stop - start))

    for classifier in classifiers:
        print('accuracy of ' + classifier + ': ' + str(statistics.mean(accuracies[classifier])))
        print('running time of ' + classifier + ': ' + str(statistics.mean(running_time[classifier])))


def choose_reduction_factor(data, k, classifier):
    reduction_percentages = [0.01, 0.03, 0.05, 0.1, 0.2, 0.3]

    # 10-fold cross validation
    accuracies = {}
    running_time = {}
    index = 0
    step = int(len(data) / 10)
    random.shuffle(data)

    for rp in reduction_percentages:
        accuracies[rp] = []
        running_time[rp] = []

    for i in range(10):
        print("training model #" + str(i + 1))
        train = data[:index] + data[index + step:]
        test = data[index:index + step]
        index = index + step

        for rp in reduction_percentages:
            start = time.time()
            pipeline = training(train, k, classifier, rp)
            accuracy = testing(test, k, pipeline)
            stop = time.time()
            accuracies[rp].append(accuracy)
            running_time[rp].append((stop - start))

    for rp in reduction_percentages:
        print("Reduction Factor: " + str(rp))
        print('accuracy: ' + str(statistics.mean(accuracies[rp])))
        print('running time: ' + str(statistics.mean(running_time[rp])))
        print('\n')

    return


if __name__ == "__main__":
    with open('../Datasets/Virus-Host/processed/families.txt', "rb") as fp:
        data = pickle.load(fp)

    # print("---------------------------- Value of K: 4 ---------------------------- ")
    # choose_classifier(data, 4, 0.1)
    #
    # print("---------------------------- Value of K: 5 ---------------------------- ")
    # choose_classifier(data, 5, 0.1)
    #
    # print("---------------------------- Value of K: 6 ---------------------------- ")
    # choose_classifier(data, 6, 0.1)
    #
    # print("---------------------------- Value of K: 7 ---------------------------- ")
    # choose_classifier(data, 7, 0.1)

    choose_reduction_factor(data, 6, 'linear-svm')
