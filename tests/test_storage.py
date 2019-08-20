
import os
import pytest

from assertpy import assert_that
from context import storage
# TODO Mock GCS
LOCAL_DATA_DIR = os.path.abspath(os.path.join('tests', 'data'))
get_local_filename = lambda f: os.path.join(LOCAL_DATA_DIR, f)
get_temp_local_filename = lambda f: storage.helpers.get_temp_filename(f)

TEST_BUCKET = 'test-lake'
#TEST_BUCKET = 'leap-test-data'
TEST_SUBDIRECTORY = 'storage_data'
JSON_FILE = 'file1.json'
CSV_FILE = 'file2.csv'
TSV_FILE = 'file2.tsv'
FILES = [JSON_FILE, CSV_FILE, TSV_FILE]
JSON_DATA = storage.json.read_json(get_local_filename(JSON_FILE))
CSV_DATA = storage.csv.read_csv(get_local_filename(CSV_FILE))
TSV_DATA = storage.csv.read_csv(get_local_filename(TSV_FILE))

GUID = 'TODO'

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

def test_get_json_from_local():
    local_file = get_local_filename(JSON_FILE)
    assert_that(storage.get(local_file)).is_equal_to(JSON_DATA)

def test_get_csv_from_local():
    local_file = get_local_filename(CSV_FILE)
    assert_that(storage.get(local_file)).is_equal_to(CSV_DATA)

def test_get_tsv_from_local():
    local_file = get_local_filename(TSV_FILE)
    assert_that(storage.get(local_file)).is_equal_to(TSV_DATA)

# listdir tests
def test_listdir_gcs():
    assert_that(sorted(storage.listdir(REMOTE_DATA_DIR))).is_equal_to(sorted(FILES))

def test_listdir_local():
    assert_that(sorted(storage.listdir(LOCAL_DATA_DIR))).is_equal_to(sorted(FILES))

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
