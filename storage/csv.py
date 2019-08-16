
import os
import csv
import numpy as np
from itertools import chain

get_delimiter = lambda f: '\t' if os.path.splitext(f)[-1] == '.tsv' else ','

def save_csv(data, filename, fieldnames = None):
    delimiter = get_delimiter(filename)
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

def read_csv(filename: str):
    delimiter = get_delimiter(filename)
    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [row for row in reader]

