import time
import numpy as np
import matplotlib.pyplot as plt
from mplcache.check_cache import compute_figure_checksum


def main():
    fig, ax = plt.subplots()
    xs = np.arange(1000)
    ax.plot(xs, xs**2)
    t1 = time.time()
    print(compute_figure_checksum(fig))
    t2 = time.time()
    print(t2 - t1)


if __name__ == '__main__':
    main()
