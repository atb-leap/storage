
import os
import tempfile

get_extension = lambda f: os.path.splitext(f)[-1]
get_filename = lambda f: os.path.basename(f)
get_temp_filename = lambda f: os.path.join(tempfile.mkdtemp(), os.path.basename(f))
