import tempfile
import unittest
import subprocess

import matplotlib.text
from mplcache.check_cache import compute_file_hash, compute_figure_checksum


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


class TextChecksumTest(unittest.TestCase):
    def test_vary_text(self):
        text = matplotlib.text.Text(0, 0, 'a')
        ck1 = compute_figure_checksum(text)
        text.set_text('b')
        ck2 = compute_figure_checksum(text)
        self.assertNotEqual(ck1, ck2)
