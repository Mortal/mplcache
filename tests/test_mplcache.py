import tempfile
import unittest
import subprocess

from mplcache.check_cache import compute_file_hash

import matplotlib.pyplot as plt


class FileHashTest(unittest.TestCase):
    def test_same_as_git(self):
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(b'Hello World!\n')
            fp.flush()
            fp.seek(0)
            our_hash = compute_file_hash(fp)
            git_hash = subprocess.check_output(
                ('git', 'hash-object', fp.name)).decode('ascii').strip()
            self.assertEqual(our_hash, git_hash)
