from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

classifiers = ["Programming Language :: Python",
               "License :: OSI Approved :: Apache Software License",
               "Development Status :: 4 - Beta"]


setup(name='spool',
      version='0.0.1',
      url='https://github.com/tOkeshu/spool',
      packages=find_packages(),
      long_description=README,
      description="A bunch of spools to tidy up your threads",
      author="Romain Gauthier",
      author_email="romain.gauthier@monkeypatch.me",
      include_package_data=True,
      py_modules=['spool'],
      classifiers=classifiers)
