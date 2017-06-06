from setuptools import setup
from raster import __doc__ as DESCRIPTION


headline = DESCRIPTION.split('\n', 1)[0].rstrip('.')


setup(
    name='mplcache',
    version='0.1',
    description=headline,
    long_description=DESCRIPTION,
    author='https://github.com/Mortal',
    url='https://github.com/Mortal/mplcache',
    packages=['mplcache'],
    include_package_data=True,
    license='GPLv3',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
