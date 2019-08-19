
A simple storage library that can get and save files locally and to GCP. The input and output of this module is formated as a dictionary.

## Getting started
 - `pip install --upgrade -e git+https://github.com/atb-leap/storage.git#egg=storage`
 - Setup your GCP credentials `export GOOGLE_APPLICATION_CREDENTIALS="[/path/to/your/credentials.json]"`
```python3
# Demo application that transfers a csv file from GCS to a local json file
import storage
input_file = 'gs://your-bucket/your/file.csv'
output_file = 'some/local/file.json'
data = storage.get(input_file)
storage.save(data, output_file)
```

## Developers
### Getting started
 - `python3 -m venv venv && source venv/bin/activate` (Optional but recommended)
 - `pip install -r requirements.txt`
