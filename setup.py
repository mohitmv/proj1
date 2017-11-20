
from setuptools import setup

setup(
	name='proj1',
	version="1.0.0",
	url='https://github.com/mohitmv/proj1',
	author='Mohit Saini',
	author_email='mohitsaini1196@gmail.com',
	description='proj1',
	long_description='proj1',
	packages=['proj1'],
	install_requires=["msl==1.0.0"],
	dependency_links = [
		"https://github.com/mohitmv/msl3/tarball/master#egg=msl-1.0.0"
	], 
	extras_require={}, 
	classifiers=[
		'Programming Language :: Python :: 3',
	],
	entry_points={}
)

