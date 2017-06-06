import tempfile
import unittest
import subprocess

import matplotlib.text
from mplcache.check_cache import compute_file_hash, compute_figure_checksum
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


class TextChecksumTest(unittest.TestCase):
    def test_vary_text(self):
        text = matplotlib.text.Text(0, 0, 'a')
        ck1 = compute_figure_checksum(text)
        text.set_text('b')
        ck2 = compute_figure_checksum(text)
        self.assertNotEqual(ck1, ck2)


class FigsizeChecksumTest(unittest.TestCase):
    def test_vary_figsize(self):
        fig1 = plt.figure(figsize=(1, 1))
        ax1 = fig1.add_subplot(111)
        ax1.plot([1, 2], [1, 2])
        ck1 = compute_figure_checksum(fig1)
        fig2 = plt.figure(figsize=(2, 1))
        ax2 = fig2.add_subplot(111)
        ax2.plot([1, 2], [1, 2])
        ck2 = compute_figure_checksum(fig2)
        self.assertNotEqual(ck1, ck2)
