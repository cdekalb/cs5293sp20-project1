from setuptools import setup, find_packages

setup(
	name='project1',
	version='1.0',
	author='Creighton DeKalb',
	authour_email='cdekalb@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)