from setuptools import setup

try:
	with open('README.md', 'r') as ldf:
		long_desc = ldf.read()
except FileNotFoundError:
	with open('README.rst', 'r') as ldf:
		long_desc = ldf.read().replace('\n', '')

setup(name='pyjazz',
	version					= '0.2.1.99',
	description				= 'Official Python client for Jazz',
	long_description		= long_desc,
	url						= 'http://github.com/kaalam/jazz',
	author					= 'kaalam.ai',
	author_email			= 'kaalam@kaalam.ai',
	license					= 'Apache 2.0',
	packages				= ['pyjazz'],
	package_data			= {'pyjazz': ['_jazz_blocks2.so', '_jazz_blocks3.so']},
	include_package_data	= True,
	zip_safe				= False,
	classifiers			    = [
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'Intended Audience :: Education',
		'Intended Audience :: Financial and Insurance Industry',
		'Intended Audience :: Healthcare Industry',
		'Intended Audience :: Information Technology',
		'Intended Audience :: Manufacturing',
		'Intended Audience :: Science/Research',
		'Intended Audience :: System Administrators',
		'Intended Audience :: Telecommunications Industry',
		'License :: OSI Approved :: Apache Software License',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3',
		'Topic :: Scientific/Engineering :: Artificial Intelligence'
      ],
	)
