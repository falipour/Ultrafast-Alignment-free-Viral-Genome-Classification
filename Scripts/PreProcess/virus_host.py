# This script pre-process virus-host db
# dependencies
import pickle
from Bio import SeqIO
from Scripts.PreProcess.utils_preprocess import delete_under_represented_classes, delete_over_represented_classes, \
    get_stat, \
    plot_data


def read_data_family(records, min_length, max_length):
    labels = []
    sequences = []

    # keeping only the sequences with length between min_length and max_length
    # removing unclassified viruses
    for virus in records:
        if max_length > len(virus.seq) > min_length:
            if len(virus.description.split("; ")) < 3:
                continue
            else:
                label = virus.description.split("; ")[2].split("|")[0]
                if "unclassified" not in label and label in valid_families:
                    labels.append(label)
                    sequences.append(str(virus.seq).upper())

                label = virus.description.split("; ")[1].split("|")[0]
                if "unclassified" not in label and label in valid_families:
                    labels.append(label)
                    sequences.append(str(virus.seq).upper())

            if len(virus.description.split("; ")) < 4:
                continue
            else:
                label = virus.description.split("; ")[3].split("|")[0]
                if "unclassified" not in label and label in valid_families:
                    labels.append(label)
                    sequences.append(str(virus.seq).upper())

    # Creating a list of tuple as the input
    data = []
    for i in range(len(sequences)):
        data.append((labels[i], sequences[i]))

    return data


def read_data_host(records, family, min_length, max_length):
    labels = []
    sequences = []

    # keeping only the sequences with length between min_length and max_length
    # removing unclassified viruses
    if family == 'Geminiviridae':
        for virus in records:
            if max_length > len(virus.seq) > min_length:
                if family in virus.description:
                    if virus.description.split("|")[3].split('; ')[-1]:
                        label = virus.description.split("|")[3].split('; ')[-1].split(" ")[0]
                        if label == 'Lycopersicon':
                            label = 'Solanum'
                        if label != 'Papilionoideae' and label != 'Streptophytina' and label != 'Solanales':
                            sequences.append(str(virus.seq).upper())
                            labels.append(label)
    else:
        for virus in records:
            if max_length > len(virus.seq) > min_length:
                if family in virus.description:
                    if virus.description.split("|")[3].split('; ')[-1]:
                        label = virus.description.split("|")[3].split('; ')[-1].split(" ")[0]
                        sequences.append(str(virus.seq).upper())
                        labels.append(label)

    # Creating a list of tuple as the input
    data = []
    for i in range(len(sequences)):
        data.append((labels[i], sequences[i]))

    return data


if __name__ == '__main__':
    # This file contain all virus families from NCBI taxonomy browser
    with open('../../Datasets/Virus-Host/valid_families.txt', "rb") as fp:
        valid_families = pickle.load(fp)

    #################################################################################################
    # Reading the data from file as SeqIO instance
    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_family = read_data_family(records, 2000, 50000)

    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_host_Geminiviridae = read_data_host(records, 'Geminiviridae', 2000, 50000)
    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_host_Caliciviridae = read_data_host(records, 'Caliciviridae', 2000, 50000)
    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_host_Reoviridae = read_data_host(records, 'Reoviridae', 2000, 50000)
    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_host_Papillomaviridae = read_data_host(records, 'Papillomaviridae', 2000, 50000)
    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_host_Polydnaviridae = read_data_host(records, 'Polydnaviridae', 2000, 50000)
    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_host_Podoviridae = read_data_host(records, 'Podoviridae', 2000, 50000)
    records = SeqIO.parse('../../Datasets/Virus-Host/virushostdb.formatted.genomic.fna', "fasta")
    data_host_Siphoviridae = read_data_host(records, 'Siphoviridae', 2000, 50000)


    #################################################################################################
    # balance the data
    data_family = delete_under_represented_classes(data_family, 100)
    data_family = delete_over_represented_classes(data_family, 500)

    data_host_Geminiviridae = delete_under_represented_classes(data_host_Geminiviridae, 10)
    data_host_Geminiviridae = delete_over_represented_classes(data_host_Geminiviridae, 50)

    data_host_Caliciviridae = delete_under_represented_classes(data_host_Caliciviridae, 10)
    data_host_Caliciviridae = delete_over_represented_classes(data_host_Caliciviridae, 50)

    data_host_Reoviridae = delete_under_represented_classes(data_host_Reoviridae, 10)
    data_host_Reoviridae = delete_over_represented_classes(data_host_Reoviridae, 50)

    data_host_Papillomaviridae = delete_under_represented_classes(data_host_Papillomaviridae, 10)
    data_host_Papillomaviridae = delete_over_represented_classes(data_host_Papillomaviridae, 50)

    data_host_Polydnaviridae = delete_under_represented_classes(data_host_Polydnaviridae, 10)
    data_host_Polydnaviridae = delete_over_represented_classes(data_host_Polydnaviridae, 50)

    data_host_Podoviridae = delete_under_represented_classes(data_host_Podoviridae, 10)
    data_host_Podoviridae = delete_over_represented_classes(data_host_Podoviridae, 50)

    data_host_Siphoviridae = delete_under_represented_classes(data_host_Siphoviridae, 10)
    data_host_Siphoviridae = delete_over_represented_classes(data_host_Siphoviridae, 50)

    #################################################################################################
    # get statistic about data
    get_stat(data_family)
    plot_data(data_family, "Virus Families", "Virus Family")

    get_stat(data_host_Geminiviridae)
    plot_data(data_host_Geminiviridae, "Geminiviridae Hosts", "Geminiviridae Host")

    get_stat(data_host_Caliciviridae)
    plot_data(data_host_Caliciviridae, "Caliciviridae Hosts", "Caliciviridae Host")

    get_stat(data_host_Reoviridae)
    plot_data(data_host_Reoviridae, "Reoviridae Hosts", "Reoviridae Host")

    get_stat(data_host_Papillomaviridae)
    plot_data(data_host_Papillomaviridae, "Papillomaviridae Hosts", "Papillomaviridae Host")

    get_stat(data_host_Polydnaviridae)
    plot_data(data_host_Polydnaviridae, "Polydnaviridae Hosts", "Polydnaviridae Host")

    get_stat(data_host_Podoviridae)
    plot_data(data_host_Podoviridae, "Podoviridae Hosts", "Podoviridae Host")

    get_stat(data_host_Siphoviridae)
    plot_data(data_host_Siphoviridae, "Siphoviridae Hosts", "Siphoviridae Host")

    #################################################################################################
    # Saving the data
    with open("../../Datasets/Virus-Host/processed/families.txt", "wb") as fp:
        pickle.dump(data_family, fp)

    with open("../../Datasets/Virus-Host/processed/geminiviridae.txt", "wb") as fp:
        pickle.dump(data_host_Geminiviridae, fp)

    with open("../../Datasets/Virus-Host/processed/caliciviridae.txt", "wb") as fp:
        pickle.dump(data_host_Caliciviridae, fp)

    with open("../../Datasets/Virus-Host/processed/reoviridae.txt", "wb") as fp:
        pickle.dump(data_host_Reoviridae, fp)

    with open("../../Datasets/Virus-Host/processed/papillomaviridae.txt", "wb") as fp:
        pickle.dump(data_host_Papillomaviridae, fp)

    with open("../../Datasets/Virus-Host/processed/polydnaviridae.txt", "wb") as fp:
        pickle.dump(data_host_Polydnaviridae, fp)

    with open("../../Datasets/Virus-Host/processed/podoviridae.txt", "wb") as fp:
        pickle.dump(data_host_Podoviridae, fp)

    with open("../../Datasets/Virus-Host/processed/siphoviridae.txt", "wb") as fp:
        pickle.dump(data_host_Siphoviridae, fp)
