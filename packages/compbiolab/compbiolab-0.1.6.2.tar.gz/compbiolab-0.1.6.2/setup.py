from setuptools import setup

setup(name='compbiolab',
      version='0.1.6.2',
      description='Common functions for the CompBioLab researchers',
      url='https://github.com/miqueleg/compbiolab',
      author='Miquel Estevez',
      author_email='miquel.estevez@udg.edu',
      license='MIT',
      packages=['compbiolab'],
      install_requires=[
                        'pytraj',
                        'pandas',
                        'matplotlib',
                        'seaborn',
                        'numpy',
                        'scipy',
                        ],
      zip_safe=False)
