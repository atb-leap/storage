
import os
from assertpy import assert_that
from context import storage
# TODO Mock GCS
LOCAL_DATA_DIR = os.path.abspath(os.path.join('tests', 'data'))
get_local_filename = lambda f: os.path.join(LOCAL_DATA_DIR, f)

TEST_BUCKET = 'test-lake'
#TEST_BUCKET = 'leap-test-data'
TEST_SUBDIRECTORY = 'storage_data'
FILES = ['file1.json', 'file2.csv']
DATA = [storage.json.read_json(get_local_filename(FILES[0])), storage.csv.read_csv(get_local_filename(FILES[1]))]

REMOTE_DATA_DIR = 'gs://{}/{}'.format(TEST_BUCKET, TEST_SUBDIRECTORY)
get_gcs_filename = lambda f: '{}/{}'.format(REMOTE_DATA_DIR, f)

# Get tests
def test_get_json_from_gcs():
    remote_file = get_gcs_filename(FILES[0])
    assert_that(storage.get(remote_file)).is_equal_to(DATA[0])

def test_get_csv_from_gcs():
    remote_file = get_gcs_filename(FILES[1])
    assert_that(storage.get(remote_file)).is_equal_to(DATA[1])

def test_get_json_from_local():
    local_file = get_local_filename(FILES[0])
    assert_that(storage.get(local_file)).is_equal_to(DATA[0])

def test_get_csv_from_local():
    local_file = get_local_filename(FILES[1])
    assert_that(storage.get(local_file)).is_equal_to(DATA[1])

# Save tests

# listdir tests
def test_listdir_gcs():
    assert_that(storage.listdir(REMOTE_DATA_DIR)).is_equal_to(FILES)

def test_listdir_local():
    assert_that(storage.listdir(LOCAL_DATA_DIR)).is_equal_to(FILES)
