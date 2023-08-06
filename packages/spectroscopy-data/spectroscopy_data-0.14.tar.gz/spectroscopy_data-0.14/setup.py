from setuptools import setup
import io, os


VERSION='0.14'

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


setup(name='spectroscopy_data',
     version=VERSION,
     description='Provides data to go along with spectroscopy.ramer.at',
     long_description = long_description,
     url='https://github.com/GeorgRamer/spectroscopy_data',
     download_url='https://github.com/GeorgRamer/spectroscopy_data/archive/{}.tar.gz'.format(VERSION),
     author='Georg Ramer',
     author_email='georg.ramer@gmail.com',
     classifiers=['Development Status :: 4 - Beta',
                  'Topic :: Scientific/Engineering',
                  'Intended Audience :: Science/Research',
                  'Intended Audience :: Education',
                  'Programming Language :: Python :: 3'],
    packages=['spectroscopy_data'],
    install_requires=['numpy','scipy'],
    python_requires='>=3.6',
    include_package_data=True)
