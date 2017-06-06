'''\
Artist hasher for matplotlib

The ArtistHasher records hashes of rendered artists.
If two renders of a figure give the same hash, then the figures are equal.
This can be used as a preprocessing step before invoking a more expensive
renderer.

    >>> import matplotlib.pyplot as plt
    >>> from mplcache.visitor import ArtistHasher
    >>> hasher = ArtistHasher()
    >>> fig, ax = plt.subplots()
    >>> lines = ax.plot([0, 1], [1, 0], 'o')
    >>> hasher.visit(fig)
    >>> print(hasher.hash)
    4082641862
'''

from mplcache.check_cache import savefig, get_timings, print_timings
