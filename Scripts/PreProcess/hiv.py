import pickle
from Bio import SeqIO
from Scripts.PreProcess.utils_preprocess import delete_under_represented_classes, delete_over_represented_classes, \
    get_stat, \
    plot_data


def read_data(records, min_length, max_length):
    labels = []
    sequences = []

    # keeping only the sequences with length between min_length and max_length
    for virus in records:
        if max_length > len(virus.seq) > min_length:
            label = virus.description
            labels.append(label)
            sequences.append(str(virus.seq).upper())

    # Creating a list of tuple as the input
    data = []
    for i in range(len(sequences)):
        data.append((labels[i], sequences[i]))

    return data


if __name__ == '__main__':
    records = SeqIO.parse('../../Datasets/HIV/HIV.fasta', "fasta")

    data = read_data(records, 2000, 50000)

    # balance the data
    data = delete_under_represented_classes(data, 20)
    # data = delete_over_represented_classes(data, 300)


    # get statistic about data
    get_stat(data)
    plot_data(data, "HIV subtypes", "HIV-1 subtype")


    # Saving the data
    with open("../../Datasets/HIV/processed/hiv.txt", "wb") as fp:
        pickle.dump(data, fp)

