# Dependencies
import time
import pickle
import random
import statistics
from Scripts.utils import training, testing

if __name__ == "__main__":
    data = None
    while not data:
        dataset = input("Please select one of the datasets from \"families\", \"geminiviridae\", "
                        "\"caliciviridae\", \"papillomaviridae\", \"podoviridae\", \"polydnaviridae\", "
                        "\"reoviridae\", \"siphoviridae\", "
                        "\"hiv\", \"dengue\"\n")

        if dataset == "families":
            with open('../Datasets/Virus-Host/processed/families.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "geminiviridae":
            with open('../Datasets/Virus-Host/processed/geminiviridae.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "caliciviridae":
            with open('../Datasets/Virus-Host/processed/caliciviridae.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "papillomaviridae":
            with open('../Datasets/Virus-Host/processed/papillomaviridae.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "podoviridae":
            with open('../Datasets/Virus-Host/processed/podoviridae.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "polydnaviridae":
            with open('../Datasets/Virus-Host/processed/polydnaviridae.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "reoviridae":
            with open('../Datasets/Virus-Host/processed/reoviridae.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "siphoviridae":
            with open('../Datasets/Virus-Host/processed/siphoviridae.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "hiv":
            with open('../Datasets/HIV/processed/hiv.txt', "rb") as fp:
                data = pickle.load(fp)

        elif dataset == "dengue":
            with open('../Datasets/Dengue/processed/dengue.txt', "rb") as fp:
                data = pickle.load(fp)

        else:
            print("Invalid dataset")

        k = 6
        rp = 0.05
        classifier = 'linear-svm'

        # 10-fold cross validation
        accuracies = []
        running_time = []
        index = 0
        step = int(len(data) / 10)
        random.shuffle(data)

        for i in range(10):
            print("training model #" + str(i + 1))
            train = data[:index] + data[index + step:]
            test = data[index:index + step]
            index = index + step

            start = time.time()
            pipeline = training(train, k, classifier, rp)
            accuracy = testing(test, k, pipeline)
            stop = time.time()
            accuracies.append(accuracy)
            running_time.append((stop - start))

        print('accuracy: ' + str(statistics.mean(accuracies)))
        print('running time: ' + str(statistics.mean(running_time)))
        print('\n')
