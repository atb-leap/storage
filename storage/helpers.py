
import os
import tempfile

FULLY_SUPPORTED_FILES = ['.json', '.tsv', '.csv']

get_extension = lambda f: os.path.splitext(f)[-1]
get_filename = lambda f: os.path.basename(f)
get_temp_filename = lambda f: os.path.join(tempfile.mkdtemp(), os.path.basename(f))
is_fully_supported_filetype = lambda f: get_extension(f) in FULLY_SUPPORTED_FILES
is_blob = lambda f: not is_fully_supported_filetype(f)
