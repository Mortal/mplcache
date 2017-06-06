import binascii
import pprint
import numpy as np


class ArtistVisitor:
    def generic_visit(self, artist):
        for c in artist.get_children():
            self.visit(c)

    def visit(self, artist):
        try:
            method = getattr(self, 'visit_' + artist.__class__.__name__)
        except AttributeError:
            method = self.generic_visit
        return method(artist)


class ArtistSerializer(ArtistVisitor):
    def visit_Line2D(self, artist):
        # if artist.get_dashes():
        #     raise NotImplementedError('Line2D.dashes')
        if artist.get_path_effects():
            raise NotImplementedError('Line2D.path_effects')
        if artist.get_clip_path():
            raise NotImplementedError('Line2D.clip_path')
        self.write(b'Line2D')
        ATTRS = '''
        alpha animated antialiased color dash_capstyle dash_joinstyle drawstyle
        fillstyle gid label linestyle linewidth marker markeredgecolor
        markeredgewidth markerfacecolor markerfacecoloralt markersize markevery
        solid_capstyle solid_joinstyle url visible zorder
        '''.split()
        for attr in ATTRS:
            v = getattr(artist, 'get_' + attr)()
            if v:
                self.write(attr.encode())
                self.write(v)
        xs, ys = artist.get_data()
        self.write(bytes(np.asarray(xs).view(np.uint8)))
        self.write(bytes(np.asarray(ys).view(np.uint8)))

    def write(self, data):
        raise NotImplementedError()


class ArtistDumper(ArtistSerializer):
    def write(self, o):
        pprint.pprint(o)


class ArtistHasher(ArtistSerializer):
    def __init__(self):
        super().__init__()
        self.hash = 0

    def write(self, o):
        if isinstance(o, bytes):
            self.hash = binascii.crc32(o, self.hash)
        elif isinstance(o, str):
            self.write(o.encode())
        elif isinstance(o, (float, int)):
            self.write(b'%r' % o)
        elif isinstance(o, (tuple, list)):
            self.write(b'%s' % len(o))
            for v in o:
                self.write(v)
        else:
            raise TypeError(type(o).__name__)


class ArtistHasherDumper(ArtistHasher):
    def __init__(self, dump_fp):
        super().__init__()
        self.dump_fp = dump_fp

    def write(self, o):
        super().write(o)
        print(self.hash, repr(o), file=self.dump_fp)
