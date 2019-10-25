
import os
import pytest
import pandas as pd
from assertpy import assert_that
from dotenv import load_dotenv
load_dotenv()

from context import storage
# TODO Mock GCS
LOCAL_DATA_DIR = os.path.abspath(os.path.join('tests', 'data'))
get_local_filename = lambda f: os.path.join(LOCAL_DATA_DIR, f)
get_temp_local_filename = lambda f: storage.helpers.get_temp_filename(f)

TEST_BUCKET = os.getenv('TEST_BUCKET')
TEST_SUBDIRECTORY = os.getenv('TEST_SUBDIRECTORY')

JSON_FILE = 'file1.json'
CSV_FILE = 'file2.csv'
TSV_FILE = 'file2.tsv'
BLOB_FILE = 'file3.txt'
FILES = [JSON_FILE, CSV_FILE, TSV_FILE, BLOB_FILE]
JSON_DATA = storage.json.read_json(get_local_filename(JSON_FILE))
JSON_DATA_RAW = storage.blob.read_blob(get_local_filename(JSON_FILE))
CSV_DATA = storage.csv.read_csv(get_local_filename(CSV_FILE))
CSV_DATA_RAW = storage.blob.read_blob(get_local_filename(CSV_FILE))
TSV_DATA = storage.csv.read_csv(get_local_filename(TSV_FILE))
BLOB_DATA = storage.blob.read_blob(get_local_filename(BLOB_FILE))

GUID = 'TEST'

REMOTE_DATA_DIR = 'gs://{}/{}'.format(TEST_BUCKET, TEST_SUBDIRECTORY)
get_gcs_filename = lambda f: '{}/{}'.format(REMOTE_DATA_DIR, f)
get_temp_gcs_filename = lambda f: get_gcs_filename('{}-{}'.format(GUID,f))

# Setup & Teardown script
class Teardown():
    def __init__(self):
        self.files_to_delete = []

    def delete(self, filename: str):
        self.files_to_delete.append(filename)

    def teardown(self):
        print('Cleaning up', self.files_to_delete)
        for f in self.files_to_delete:
            if storage.exists(f):
                storage.delete(f)


@pytest.fixture(autouse=True)
def teardown():
    #Setup
    print('Setup test')
    td = Teardown()
    yield td
    print('teardown test')
    # Teardown
    td.teardown()

# listdir tests
def test_listdir_gcs():
    assert_that(sorted(storage.listdir(REMOTE_DATA_DIR))).is_equal_to(sorted(FILES))

def test_listdir_local():
    assert_that(sorted(storage.listdir(LOCAL_DATA_DIR))).is_equal_to(sorted(FILES))

# exists tests
def test_local_exist():
    local_file = get_local_filename(JSON_FILE)
    assert_that(storage.exists(local_file)).is_true()

def test_remote_exist():
    remote_file = get_gcs_filename(JSON_FILE)
    assert_that(storage.exists(remote_file)).is_true()

def test_remote_does_not_exist():
    remote_file = get_gcs_filename('some_file_that_does_not_exist.txt')
    assert_that(storage.exists(remote_file)).is_false()

def test_local_does_not_exist():
    local_file = get_local_filename('some_file_that_does_not_exist.txt')
    assert_that(storage.exists(local_file)).is_false()

# Get tests
def test_get_json_from_gcs():
    remote_file = get_gcs_filename(JSON_FILE)
    assert_that(storage.get(remote_file)).is_equal_to(JSON_DATA)

def test_get_csv_from_gcs():
    remote_file = get_gcs_filename(CSV_FILE)
    assert_that(storage.get(remote_file)).is_equal_to(CSV_DATA)

def test_get_tsv_from_gcs():
    remote_file = get_gcs_filename(TSV_FILE)
    assert_that(storage.get(remote_file)).is_equal_to(TSV_DATA)

def test_get_blob_from_gcs():
    remote_file = get_gcs_filename(BLOB_FILE)
    assert_that(storage.get(remote_file)).is_equal_to(BLOB_DATA)

def test_get_json_from_local():
    local_file = get_local_filename(JSON_FILE)
    assert_that(storage.get(local_file)).is_equal_to(JSON_DATA)

def test_get_json_from_local_as_blob():
    local_file = get_local_filename(JSON_FILE)
    assert_that(storage.get(local_file, asBlob=True)).is_equal_to(JSON_DATA_RAW)

def test_get_csv_from_local():
    local_file = get_local_filename(CSV_FILE)
    assert_that(storage.get(local_file)).is_equal_to(CSV_DATA)

def test_get_tsv_from_local():
    local_file = get_local_filename(TSV_FILE)
    assert_that(storage.get(local_file)).is_equal_to(TSV_DATA)

def test_get_blob_from_local():
    local_file = get_local_filename(BLOB_FILE)
    assert_that(storage.get(local_file)).is_equal_to(BLOB_DATA)

# Save tests
def test_save_json_to_gcs(teardown):
    remote_file = get_temp_gcs_filename(JSON_FILE)
    teardown.delete(remote_file)
    storage.save(JSON_DATA, remote_file)
    assert_that(storage.get(remote_file)).is_equal_to(JSON_DATA)

def test_save_json_to_local(teardown):
    local_file = get_temp_local_filename(JSON_FILE)
    teardown.delete(local_file)
    storage.save(JSON_DATA, local_file)
    assert_that(storage.get(local_file)).is_equal_to(JSON_DATA)

def test_save_csv_to_gcs(teardown):
    remote_file = get_temp_gcs_filename(CSV_FILE)
    teardown.delete(remote_file)
    storage.save(CSV_DATA, remote_file)
    assert_that(storage.get(remote_file)).is_equal_to(CSV_DATA)

def test_save_csv_to_local(teardown):
    local_file = get_temp_local_filename(CSV_FILE)
    teardown.delete(local_file)
    storage.save(CSV_DATA, local_file)
    assert_that(storage.get(local_file)).is_equal_to(CSV_DATA)

def test_save_raw_csv_to_local(teardown):
    local_file = get_temp_local_filename(CSV_FILE)
    teardown.delete(local_file)
    storage.save(CSV_DATA_RAW, local_file, asBlob=True)
    assert_that(storage.get(local_file)).is_equal_to(CSV_DATA)

def test_save_pandas_to_csv(teardown):
    local_file = get_temp_local_filename(CSV_FILE)
    teardown.delete(local_file)
    storage.save(pd.DataFrame(CSV_DATA), local_file)
    assert_that(storage.get(local_file)).is_equal_to(CSV_DATA)

def test_save_tsv_to_gcs(teardown):
    remote_file = get_temp_gcs_filename(TSV_FILE)
    teardown.delete(remote_file)
    storage.save(CSV_DATA, remote_file)
    assert_that(storage.get(remote_file)).is_equal_to(TSV_DATA)

def test_save_tsv_to_local(teardown):
    local_file = get_temp_local_filename(TSV_FILE)
    teardown.delete(local_file)
    storage.save(TSV_DATA, local_file)
    assert_that(storage.get(local_file)).is_equal_to(TSV_DATA)

def test_save_blob_to_gcs(teardown):
    remote_file = get_temp_gcs_filename(BLOB_FILE)
    teardown.delete(remote_file)
    storage.save(BLOB_DATA, remote_file)
    assert_that(storage.get(remote_file)).is_equal_to(BLOB_DATA)

def test_save_blob_to_local(teardown):
    local_file = get_temp_local_filename(BLOB_FILE)
    teardown.delete(local_file)
    storage.save(BLOB_DATA, local_file)
    assert_that(storage.get(local_file)).is_equal_to(BLOB_DATA)

# Copy tests
def test_copy_local_to_remote(teardown):
    local_file = get_local_filename(BLOB_FILE)
    remote_file = get_temp_gcs_filename(BLOB_FILE)
    teardown.delete(remote_file)
    storage.copy(local_file, remote_file)
    assert_that(storage.get(remote_file)).is_equal_to(BLOB_DATA)

def test_copy_local_to_local(teardown):
    local_file = get_local_filename(BLOB_FILE)
    temp_file = get_temp_local_filename(BLOB_FILE)
    teardown.delete(temp_file)
    storage.copy(local_file, temp_file)
    assert_that(storage.get(temp_file)).is_equal_to(BLOB_DATA)

def test_copy_remote_to_local(teardown):
    local_file = get_temp_local_filename(BLOB_FILE)
    remote_file = get_gcs_filename(BLOB_FILE)
    teardown.delete(local_file)
    storage.copy(remote_file, local_file)
    assert_that(storage.get(local_file)).is_equal_to(BLOB_DATA)

def test_copy_remote_to_remote(teardown):
    remote_file = get_gcs_filename(BLOB_FILE)
    remote_temp_file = get_temp_gcs_filename(BLOB_FILE)
    teardown.delete(remote_temp_file)
    storage.copy(remote_file, remote_temp_file)
    assert_that(storage.get(remote_temp_file)).is_equal_to(BLOB_DATA)

def test_copy_remote_to_remote_with_filetype_change(teardown):
    remote_file = get_gcs_filename(CSV_FILE)
    remote_temp_file = get_temp_gcs_filename(JSON_FILE)
    teardown.delete(remote_temp_file)
    storage.copy(remote_file, remote_temp_file)
    assert_that(storage.get(remote_temp_file)).is_equal_to(CSV_DATA)

# Move tests
def test_move(teardown):
    local_file = get_local_filename(BLOB_FILE)
    temp_file = get_temp_local_filename(BLOB_FILE)
    temp_file2 = get_temp_local_filename(BLOB_FILE)
    teardown.delete(temp_file)
    teardown.delete(temp_file2)
    storage.copy(local_file, temp_file)
    storage.move(temp_file, temp_file2)
    assert_that(storage.get(temp_file2)).is_equal_to(BLOB_DATA)
    assert_that(storage.exists(temp_file)).is_false()
