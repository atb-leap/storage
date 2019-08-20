
import os
import csv
import pandas as pd
import numpy as np
from itertools import chain

get_delimiter = lambda f: '\t' if os.path.splitext(f)[-1] == '.tsv' else ','
def has_header(filename: str):
    with open(filename, 'r') as f:
        sniffer = csv.Sniffer()
        for i in range(50):
            if f.readline() is None:
                break
        bytes_to_use = f.tell()
        f.seek(0)
        data = f.read(bytes_to_use)
        has_header = sniffer.has_header(data)
        # print('{}\thas header: {}\tdelimiter: {}'.format(filename, has_header, repr(sniffer.sniff(data).delimiter)))
        return has_header

get_header = lambda filename, header: 0 if header is True or header == 'infer' and has_header(filename) else None

def save_csv(data, filename, fieldnames = None, ignore_header = False):
    delimiter = get_delimiter(filename)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as out:
        if isinstance(data[0], dict):
            if fieldnames is None:
                fieldnames = data[0].keys()
            writer = csv.DictWriter(out, delimiter=delimiter, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            if not ignore_header:
                writer.writeheader()
        else:
            writer = csv.writer(out, delimiter=delimiter, quoting=csv.QUOTE_NONNUMERIC)
            if ignore_header and csv.Sniffer().has_header('\n'.join(data[0:min(100, len(data))])):
                data = data[1:]

        writer.writerows(data)

def read_csv(filename: str, pandas=False, header='infer'):
    delimiter=get_delimiter(filename)
    header=get_header(filename, header)
    df = pd.read_csv(filename, delimiter=delimiter, header=header, quoting=csv.QUOTE_NONNUMERIC)
    if pandas:
        return df
    else:
        return df.to_dict('records')
