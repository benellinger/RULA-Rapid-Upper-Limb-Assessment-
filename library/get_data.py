
# coding: utf-8
#!/usr/bin/env python
"""
module for importing data and analyzing due to rula
"""

import numpy as np
import csv
import re


def get_data(fID):
    """Function ro read MR3 and QTM files

    input needs to be *.csv or *.tsv. Required decimal separator is "."
    Returns file information (dict), header information (dict) and data (np.array)
    """
    info = dict()
    with open(fID, encoding='utf-8') as csvfile:
        print(fID)
        try:
            if re.search(".csv", fID):
                delimiter = ";"
                csvcontent = csv.reader(csvfile, delimiter=delimiter)
                for a,row in enumerate(csvcontent):
                    if row[0] == "Name":
                        info[row[0]] = row[1]
                    elif row[0] == "Frequency":
                        info[row[0]] = row[1]
                    elif row[0] == "Date":
                        info[row[0]] = row[1]
                    elif re.search("Time", row[0]):
                        header = np.array(row)
                        break

            elif re.search(".tsv", fID):
                delimiter = "\t"
                csvcontent = csv.reader(csvfile, delimiter=delimiter)
                for a,row in enumerate(csvcontent):
                    if row[0] == "Frame":
                        header = np.array(row)
                        a += 1
                        break
                    else:
                        info[row[0]] = row[1::]

            data = np.genfromtxt(fID, delimiter=delimiter, skip_header=a+1, dtype=np.float64)
        except:
            print("could not load data. Loading capturing information failed. Please check file format.")


    print(info)
    return info, header, data



def read_all_files(fID):
    """Generates a list of paths to files

    inuput is ASCII file; file must contain paths to other files
    """
    file_list = []
    with open(fID, encoding='utf-8') as current_file:
        for line in current_file:
            line = line.replace('\n', '')
            file_list.append(line)

    return file_list



def moving_average_1D(data, window):
    """smooths data according to moving average algorithm

    input should be array or list; returns 1-D array
    """
    smoothed_array = np.zeros(len(data)-window)
    for i in range(len(smoothed_array)):
        smoothed_array[i] = np.mean(data[i, i+window])

    return smoothed_array
