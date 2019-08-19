
import os
import tempfile

SUPPORTED_FILE_TYPES = ['.json', '.tsv', '.csv']

get_extension = lambda f: os.path.splitext(f)[-1]
get_filename = lambda f: os.path.basename(f)
is_supported_file_format = lambda f: True if get_extension(f) in SUPPORTED_FILE_TYPES else False
get_temp_filename = lambda f: os.path.join(tempfile.mkdtemp(), os.path.basename(f))
