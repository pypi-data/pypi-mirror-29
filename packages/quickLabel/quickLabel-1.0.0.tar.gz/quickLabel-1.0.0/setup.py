from setuptools import setup

setup(
   name='quickLabel',
   version='1.0.0',
   description='A tool for image labeling',
   author='Alexey Vlaskin',
   author_email='alex@avlaskin.com',
   url='https://github.com/avlaskin',
   packages=['quickLabel'],  #same as name
   install_requires=['pillow'], #external packages as dependencies
)
