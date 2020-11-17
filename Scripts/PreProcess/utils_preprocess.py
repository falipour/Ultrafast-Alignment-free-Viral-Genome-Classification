# collection of small python helper functions which make common patterns shorter and easier
import matplotlib.pyplot as plt
import json


# build a dict of labels and their occurrences from a list of tuples of labels and sequences
def count_class_occurrences(data):
    unique_labels = list(set(map(lambda x: x[0], data)))
    class_occurrences = {}

    for label in unique_labels:
        class_occurrences[label] = 0

    for virus in data:
        class_occurrences[virus[0]] += 1

    return class_occurrences


# delete all the under-represented classes
def delete_under_represented_classes(data, min_elements):
    class_occurrences = count_class_occurrences(data)

    i = 0
    while i < len(data):
        if class_occurrences[data[i][0]] < min_elements:
            data.pop(i)
        else:
            i += 1

    return data


# delete all the over-represented classes
def delete_over_represented_classes(data, max_elements):
    class_occurrences = count_class_occurrences(data)

    i = 0
    overrepresented_classes = []
    while i < len(data):
        if class_occurrences[data[i][0]] > max_elements:
            if data[i][0] not in overrepresented_classes:
                overrepresented_classes.append(data[i][0])
        i += 1

    delete = False
    for label in overrepresented_classes:
        count = 0
        i = 0
        while i < len(data):
            if count == max_elements:
                delete = True
            if data[i][0] == label:
                if not delete:
                    count += 1
                    i += 1
                else:
                    data.pop(i)
            else:
                i += 1

    return data


def get_stat(data):
    class_occurrences = count_class_occurrences(data)

    max_len = 0
    min_len = 1000000
    for i in range(len(data)):
        if len(data[i][1]) < min_len:
            min_len = len(data[i][1])
        if len(data[i][1]) > max_len:
            max_len = len(data[i][1])

    print("---------- Sequences Stats ----------")
    print("Total number of sequences: " + str(len(data)))
    print("Minimum length: " + str(min_len))
    print("Maximum length: " + str(max_len) + "\n")
    print("---------- Classes Stats ----------")
    print("Total number of classes: " + str(len(class_occurrences.keys())))
    print("Class Occurrences:")
    print(json.dumps(class_occurrences, indent=4, sort_keys=True))


def plot_data(data, title, xlabel):
    class_occurrences = count_class_occurrences(data)

    plt.bar(range(len(class_occurrences)), class_occurrences.values(), align='center', color=(0.2, 0.4, 0.6, 0.6))
    plt.xticks(range(len(class_occurrences)), list(class_occurrences.keys()))
    plt.xticks(rotation=90)
    # plt.title("Distribution of " + title + " dataset")
    plt.xlabel(xlabel)
    plt.ylabel("Count")
    plt.show()
