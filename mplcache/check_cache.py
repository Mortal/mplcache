import os
import time
import hashlib
from mplcache.visitor import ArtistHasher, ArtistHasherDumper
import contextlib
import shutil


def get_cache_home():
    '''
    Get the directory in which we store our cached files.
    '''
    try:
        return get_cache_home._value
    except AttributeError:
        pass
    try:
        cache_base = os.environ['XDG_CACHE_HOME']
    except KeyError:
        cache_base = os.path.expanduser('~/.cache')
    cache_dir = os.path.join(cache_base, 'mplcache')
    os.makedirs(cache_dir, exist_ok=True)
    get_cache_home._value = cache_dir
    return cache_dir


def set_cache_home(d):
    '''
    Set the directory where we should look for and store cached files.
    '''
    get_cache_home._value = d


def get_path(*args):
    '''
    Construct a path inside our cache directory.
    '''
    return os.path.join(get_cache_home(), *args)


def compute_file_hash(fileobj):
    '''
    Compute a SHA-1 hash for the given open file.

    Uses the same algorithm as Git.
    '''
    h = hashlib.sha1()
    size = os.fstat(fileobj.fileno()).st_size
    h.update(('blob %s\0' % size).encode('ascii'))
    while True:
        s = fileobj.read(2**16)
        if s == b'':
            break
        h.update(s)
    return h.hexdigest()


def get_file_hash(path):
    with open(path, 'rb') as fp:
        return compute_file_hash(fp)


def get_file_hash_path(path):
    file_hash = get_file_hash(path)
    return get_path(file_hash[:2], file_hash[2:])


def get_figure_checksum(path):
    hash_path = get_file_hash_path(path)
    try:
        with open(hash_path) as fp:
            return hash_path, fp.read().strip()
    except FileNotFoundError:
        return hash_path, None


def save_checksum(path, figure_checksum):
    file_hash_path, old_figure_checksum = get_figure_checksum(path)
    if figure_checksum == old_figure_checksum:
        return
    elif old_figure_checksum is not None:
        print("WARNING: File hash collision",
              path, file_hash_path, old_figure_checksum, figure_checksum)

    os.makedirs(os.path.dirname(file_hash_path), exist_ok=True)

    tmp = file_hash_path + '.tmp'
    with open(tmp, 'w') as fp:
        fp.write('%s\n' % figure_checksum)
    os.rename(tmp, file_hash_path)

    return file_hash_path


def compute_figure_checksum(fig: 'matplotlib.figure.Figure', dump_fp=None):
    if dump_fp is None:
        visitor = ArtistHasher()
    else:
        visitor = ArtistHasherDumper(dump_fp)
    visitor.visit(fig)
    return str(visitor.hash)


def savefig(fig: 'matplotlib.figure.Figure', path):
    try:
        t1 = time.time()
        old_hash_path, old_figure_checksum = get_figure_checksum(path)
        t2 = time.time()
        elapsed_read_old = t2 - t1
    except FileNotFoundError:
        old_figure_checksum = None
        elapsed_read_old = None

    with contextlib.ExitStack() as stack:
        if os.environ.get('MPLCACHE_DUMP'):
            dump_path = old_hash_path + '_new.txt'
            print("Dump to", dump_path)
            os.makedirs(os.path.dirname(dump_path), exist_ok=True)
            dump_fp = stack.enter_context(open(dump_path, 'w'))
        else:
            dump_path = dump_fp = None
        t1 = time.time()
        figure_checksum = compute_figure_checksum(fig, dump_fp)
        t2 = time.time()
        elapsed_checksum = t2 - t1

    if figure_checksum != old_figure_checksum:
        t1 = time.time()
        fig.savefig(path)
        t2 = time.time()
        elapsed_real = t2 - t1

        t1 = time.time()
        new_hash_path = save_checksum(path, figure_checksum)
        t2 = time.time()
        elapsed_read_new = t2 - t1

        if dump_path is not None:
            shutil.copyfile(dump_path, new_hash_path + '_old.txt')

        savefig.timings.append(
            (elapsed_read_old, elapsed_checksum, elapsed_real, elapsed_read_new))
    else:
        savefig.timings.append(
            (elapsed_read_old, elapsed_checksum, None, None))


savefig.timings = []


def get_timings():
    r = savefig.timings[:]
    del savefig.timings[:]
    return r


def print_timings():
    t1, t2, t3, t4 = zip(*get_timings())

    def help(name, values):
        values = [v for v in values if v is not None]
        if values:
            print('%s %s/%s/%s (%s)' %
                  (name, min(values), sum(values) / len(values),
                   max(values), len(values)))

    help('Read old plot:', t1)
    help('Compute figure checksum:', t2)
    help('Save plot:', t3)
    help('Read new plot:', t4)
