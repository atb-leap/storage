
import os

def save_blob(data, filename, append = False):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'a' if append else 'w') as outfile:
        outfile.write(data)

def read_blob(filename):
    with open(filename, 'r') as f:
        return f.read()
