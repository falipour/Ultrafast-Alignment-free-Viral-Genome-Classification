import numpy as np
from itertools import product
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.preprocessing import normalize, StandardScaler
from sklearn import svm, discriminant_analysis, neighbors
from sklearn.neural_network import MLPClassifier


def count_kmers(sequence, k):
    kmers_dict = {}

    for kmer in product('ACGT', repeat=k):
        kmers_dict[''.join(kmer)] = 0

    for i in range(len(sequence) - k):
        try:
            kmers_dict[sequence[i:i + k]] += 1
        except KeyError:
            pass

    return list(kmers_dict.values())


def build_pipeline(num_features, classifier, reduction_factor):
    # setup normalizers if needed
    normalizers = []
    normalizers.append(('scaler', StandardScaler(with_mean=False)))

    # reduce dimensionality to some fraction of its original
    normalizers.append(('dim_reducer', TruncatedSVD(n_components=int(
        np.ceil(num_features * reduction_factor)))))

    # Classifiers

    # 10-nearest-neighbors
    if classifier == '10-nearest-neighbors':
        normalizers.append(('classifier', neighbors.KNeighborsClassifier(n_neighbors=10, metric='euclidean')))

    # nearest-centroid-mean
    if classifier == 'nearest-centroid-mean':
        normalizers.append(('classifier', neighbors.NearestCentroid(metric='euclidean')))

    # nearest-centroid-median
    if classifier == 'nearest-centroid-median':
        normalizers.append(('classifier', neighbors.NearestCentroid(metric='manhattan')))

    # logistic-regression
    if classifier == 'logistic-regression':
        normalizers.append(('classifier', LogisticRegression()))

    # linear-svm
    if classifier == 'linear-svm':
        normalizers.append(('classifier', svm.SVC(kernel='linear')))

    # quadratic-svm
    if classifier == 'quadratic-svm':
        normalizers.append(('classifier', svm.SVC(kernel='poly', degree=2)))

    # cubic-svm
    if classifier == 'cubic-svm':
        normalizers.append(('classifier', svm.SVC(kernel='poly', degree=3)))

    # sgd
    if classifier == 'sgd':
        normalizers.append(('classifier', SGDClassifier(max_iter=5)))

    # decision-tree
    if classifier == 'decision-tree':
        normalizers.append(('classifier', DecisionTreeClassifier()))

    # random-forest
    if classifier == 'random-forest':
        normalizers.append(('classifier', RandomForestClassifier(n_estimators=10)))

    # adaboost
    if classifier == 'adaboost':
        normalizers.append(('classifier', AdaBoostClassifier(n_estimators=50)))

    # gaussian-naive-bayes
    if classifier == 'gaussian-naive-bayes':
        normalizers.append(('classifier', GaussianNB()))

    # lda
    if classifier == 'lda':
        normalizers.append(('classifier', discriminant_analysis.LinearDiscriminantAnalysis()))

    # qda
    if classifier == 'qda':
        normalizers.append(('classifier', discriminant_analysis.QuadraticDiscriminantAnalysis()))

    # multilayer-perceptron
    if classifier == 'multilayer-perceptron':
        normalizers.append(('classifier', MLPClassifier(solver='sgd')))

    return Pipeline(normalizers)


def training(train_data, k, classifier, reduction_factor):
    train_features = []
    train_labels = []

    for i in range(len(train_data)):
        train_features.append(count_kmers(train_data[i][1], k))
        train_labels.append(train_data[i][0])

    x = np.asarray(train_features).astype('float32')
    x = normalize(x, norm='l2', axis=1)

    features = normalize(x, norm='l2', axis=1)
    labels = np.asarray(train_labels)

    # Run the classification Pipeline
    pipeline = build_pipeline(4 ** k, classifier, reduction_factor)
    pipeline.fit(features, labels)

    return pipeline


def testing(test_data, k, pipeline):
    test_features = []
    test_labels = []

    for i in range(len(test_data)):
        test_features.append(count_kmers(test_data[i][1], k))
        test_labels.append(test_data[i][0])

    x = np.asarray(test_features).astype('float32')
    y = np.asarray(test_labels)
    test_features = normalize(x, norm='l2', axis=1)
    y_pred = pipeline.predict(test_features)
    return accuracy_score(y, y_pred)
