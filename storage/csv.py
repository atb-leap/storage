
import os
import csv
import numpy as np

def save_csv(data, filename, fieldnames = None):
    _, extension = os.path.splitext(filename)
    if extension == '.tsv':
        delimiter = '\t'
    else:
        delimiter = ','
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as out:
        if type(data[0]) is dict:
            if fieldnames is None:
                fieldnames = np.unique(list(chain(*[d.keys() for d in data])))
            writer = csv.DictWriter(out, delimiter=delimiter, fieldnames=fieldnames)
            writer.writeheader()
        else:
            writer = csv.writer(out, delimiter=delimiter)
            if type(data[0]) is str:
                data = [[' '.join(d.split())] for d in data]
        writer.writerows(data)
