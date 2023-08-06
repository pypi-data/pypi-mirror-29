import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='filter_pandoc_run_py',
      version='0.4',
      long_description=read('README.md'),
      url='https://github.com/caiofcm/filter_pandoc_run_py',
      download_url='https://github.com/caiofcm/filter_pandoc_run_py/archive/0.1.tar.gz',
      author='Caio Marcellos',
      author_email='caiocuritiba@gmail.com',
      license='MIT',
      packages=find_packages(),
     install_requires=['pandocfilters', 'matplotlib'],
      keywords='pandoc filters markdown python notes',
      zip_safe=False,
      py_modules=["filter_pandoc_run_py.filter_pandoc_run_py"],
      entry_points={
          'console_scripts': [
              'filter_pandoc_run_py = filter_pandoc_run_py.filter_pandoc_run_py:main',
          ],
      },
      extras_require={
          'dev': ['check-manifest'],
          'test': ['coverage'],
      },
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'coverage'],
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Utilities",
          "License :: OSI Approved :: BSD License",  # to be reviewed
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',

          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
          'Topic :: Software Development :: Documentation',
          'Topic :: Text Processing :: Filters',
      ]

      # Alternatively, if you want to distribute just a my_module.py, uncomment
      # this:
)
