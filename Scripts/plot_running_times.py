import math
import matplotlib.pyplot as plt

running_times = {}

running_times['10-nearest-neighbors'] = [21.6, 24.5, 38.2, 116.8]
running_times['nearest-centroid-mean'] = [21.8, 23.6, 33.3, 101.8]
running_times['nearest-centroid-median'] = [21.5, 25.0, 33.0, 102.1]
running_times['logistic-regression'] = [26.8, 27.4, 36.9, 122.8]
running_times['linear-svm'] = [22.8, 26.9, 36.7, 166.9]
running_times['quadratic-svm'] = [21.9, 26.3, 40.4, 156.1]
running_times['cubic-svm'] = [22.2, 26.6, 42.4, 180.5]
running_times['sgd'] = [21.2, 25.9, 36.6, 123.9]
running_times['decision-tree'] = [21.5, 25.5, 38.8, 150.9]
running_times['random-forest'] = [21.8, 23.8, 38.0, 137.9]
running_times['adaboost'] = [23.4, 27.7, 52.6, 198.7]
running_times['gaussian-naive-bayes'] = [21.6, 23.8, 35.8, 168.4]
running_times['lda'] = [21.4, 22.9, 34.2, 174.6]
running_times['qda'] = [21.1, 25.2, 34.4, 147.9]
running_times['multilayer-perceptron'] = [27.1, 30.3, 46.4, 197.6]

x = [4, 5, 6, 7]

methods = running_times.keys()

for method in methods:
    plt.plot(x, running_times[method])  # plotting t, a separately

plt.legend(methods)
plt.ylabel('Running Time (s)')
plt.xlabel('k')
plt.show()