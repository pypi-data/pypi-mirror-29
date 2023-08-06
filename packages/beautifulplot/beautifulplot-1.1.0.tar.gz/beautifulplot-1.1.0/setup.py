from setuptools import setup

setup(name='beautifulplot',
      version='1.1.0',
      description='Make beautiful plot and statistical analysis effortless.',
      url='https://github.com/bgallois/BeautifulPlot',
      author='Benjamin Gallois',
      author_email='benjamin.gallois@upmc.fr',
      license='GNU GENERAL PUBLIC LICENSE',
      packages=['beautifulplot'],
      install_requires=[
          'matplotlib', 'numpy', 'scipy'
      ],
      python_requires='>=3',
      py_modules=["six"],
      zip_safe=False)