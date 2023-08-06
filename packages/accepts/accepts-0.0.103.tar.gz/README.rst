.. README generated with readmemako.py (github.com/russianidiot/readme-mako.py) and .README dotfiles (github.com/russianidiot-dotfiles/.README)


.. image:: https://img.shields.io/badge/Language-Python-blue.svg?style=plastic
	:target: none

.. image:: https://img.shields.io/pypi/pyversions/accepts.svg
	:target: https://pypi.org/pypi/accepts

.. image:: https://img.shields.io/pypi/v/accepts.svg
	:target: https://pypi.org/pypi/accepts

|

.. image:: https://api.codacy.com/project/badge/Grade/81a64e612bec41c4afe6fc3901daa88a
	:target: https://www.codacy.com/app/looking-for-a-job/accepts-py

.. image:: https://codeclimate.com/github/looking-for-a-job/accepts.py/badges/gpa.svg
	:target: https://codeclimate.com/github/looking-for-a-job/accepts.py

.. image:: https://scrutinizer-ci.com/g/looking-for-a-job/accepts.py/badges/quality-score.png?b=master
	:target: https://scrutinizer-ci.com/g/looking-for-a-job/accepts.py/

|




Install
```````


.. code:: bash

	`[sudo] pip install accepts`




Features
````````

*	support **multiple types** argument
*	support **None** argument
*	human readable detailed exception message


Usage
`````


.. code:: python

	>>> from accepts import accepts
	
	>>> @accepts(arg1type,arg2type,...)



Examples
````````


.. code:: bash

	>>> @accepts(int)
	def inc(value):
		return value+1
	
	>>> inc(1) # ok
	>>> inc(1.5) # exception
	TypeError: ....
	
	# multiple types
	>>> @accepts((int,float))
	
	# None
	>>> @accepts((int,float,None))





Feedback |github_follow| |github_issues|

.. |github_follow| image:: https://img.shields.io/github/followers/russianidiot.svg?style=social&label=Follow
	:target: https://github.com/russianidiot

.. |github_issues| image:: https://img.shields.io/github/issues/looking-for-a-job/accepts.py.svg
	:target: https://github.com/looking-for-a-job/accepts.py/issues

