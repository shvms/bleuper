with open('README.md', encoding='utf-8') as file:
    readme = file.read()

from distutils.core import setup
setup(
  name = 'bleuper',
  packages = ['bleuper'],
  version = '0.2',
  license='MIT',
  description = 'A simple lightweight library for computing BLEU scores',
  long_description = readme,
  long_description_content_type='text/markdown',
  author = 'Shuvam Shah',
  author_email = 'shuvamkshah28@gmail.com',
  url = 'https://github.com/shvms/bleuper',
  download_url = 'https://github.com/shvms/bleuper/archive/v0.2-alpha.tar.gz',
  keywords = ['BLEU', 'machine-translation', 'nlp', 'baseline'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
  tests_require=[
    'pytest>=5',
  ]
)
