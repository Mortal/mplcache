from mplcache import savefig
import matplotlib
matplotlib.use('ps')
matplotlib.rc('text', usetex=True)
import matplotlib.pyplot as plt
from mplcache.visitor import ArtistDumper


def main():
    fig, ax = plt.subplots()
    ax.plot([0, 1], [1, 0], 'o')
    # ArtistDumper().visit(fig)
    savefig(fig, 'plot.png')
    print(savefig.timings)


if __name__ == '__main__':
    main()
