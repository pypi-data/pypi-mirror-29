from distutils.core import setup
setup(
  name = 'icls',
  packages = ['icls'],
  install_requires=[
   'pandas',
   'numpy',
   'scipy',
   'tensorflow>=1.0.0'
],
  version = '0.1',
  description = 'Implicitly-Constrained Least Squares for Semi-Supervised Learning',
  author = 'David Cortes',
  author_email = 'david.cortes.rivera@gmail.com',
  url = 'https://github.com/david-cortes/icls',
  download_url = 'https://github.com/david-cortes/icls/archive/0.1.tar.gz',
  keywords = ['icls', 'implicitly constrained least squares', 'semi supervised learning'],
  classifiers = [],
)