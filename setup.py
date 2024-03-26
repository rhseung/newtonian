from newtonian import __version__, __package__
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
	long_description = f.read()
with open('requirements.txt', 'r', encoding='utf-8') as f:
	requirements = f.read().splitlines()

setup(
	name=__package__,
	version=__version__,
	long_description=long_description,
	install_requires=requirements,
	python_requires='>=3.11',
	packages=find_packages(),
	author='rhseung',
	author_email='rhseungg@gmail.com',
	url='https://github.com/rhseung/newtonian',
	keywords=['units', 'physics', 'mathematics', 'physics engine'],
)
