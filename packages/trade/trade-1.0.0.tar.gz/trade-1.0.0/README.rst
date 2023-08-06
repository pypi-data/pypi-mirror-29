trade
=====
| A framework for financial applications.
| Copyright (c) 2015-2018 Rafael da Silva Rocha
| https://python-trade.appspot.com
| https://github.com/rochars/trade

--------------

|Build| |Windows Build| |Coverage Status| |Scrutinizer| |Python Versions| |Live Demo|


Installation
------------

    $ pip install trade


trade
-----
**trade** is a framework for the creation of financial applications.


It uses the concept of *holders*, *subjects*, *occurrences* and *contexts*
--------------------------------------------------------------------------
A *subject* is anything that can be traded.

A *holder* is someone who owns subjects.

A *holder* state is update by *occurrences*.

*Occurrences* may occur alone or in *contexts*.


A *subject* is anything that can be traded
------------------------------------------
A *subject* may be the share of a corporation, livestock and so on.


A *holder* is a entity that owns subjects
-----------------------------------------
A *holder* owns subjects. The *holder* state is updated by occurrences.


*Occurrences* happen with subjects and change the state of the *holder*
-----------------------------------------------------------------------
A *occurrence* may be caused by the *holder*, like the purchase of units of some
*subject*. They can also represent third-party events, like a stock split.
In both cases they should change the state of the *holder*.


A *context* may have its own rules
----------------------------------
*Contexts* are groups of occurrences.

*Contexts* are used to pre-process occurrences before informing them to a *holder*.

A *context* may be a situation where daytrades should be identified, for example.

A *context* may also involve taxes and other costs altering the details of the occurrences.


Extending the framework
-----------------------
**trade** should be extended with new types of *occurrences* and *subjects*.

New *context rules* can be created.

The *holder* state can be modeled according to the needs of the application.

Look at the examples.


Live sample app
---------------
You can try it `live <https://python-trade.appspot.com>`_.

This is a sample app built with **trade**. It runs as a service.

The input is a JSON containing *occurrences* and a initial state
for the *holder*.

The sample app have *context tasks* to identify daytrades, apply
costs to occurrences and more.

The service also calculates the profits and losses from the occurrences
and groups the results by asset.

The output is the *holder* state as a JSON.


Use:
----
A example without the use of contexts:

.. code:: python

	from trade.holder import Holder
	from trade.occurrence import Occurrence
	from trade.subject import Subject

	# create a holder
	holder = Holder()

	# define some subject
	some_asset = Subject('AST1', {})

	# create an occurrence with that subject.
	# In this example, a purchase of 100 units of the asset,
	# for the value of $20.
	some_occurrence = Occurrence(
			some_asset,
			'2018-01-02',
			{
				"quantity": 100,
				"value": 20
			}
		)

	# pass it to the holder
	holder.trade(some_occurrence)

	# check the holder state:
	for subject, state in holder.state.items():
		print(subject)
		print(state)
	# AST1
	# {'value': 20.0, 'quantity': 100}


	# create some other occurrence with that subject.
	# In this example, a sale of 20 units of the asset,
	# for the value of $30.
	holder.trade(Occurrence(
			some_asset,
			'2018-01-03',
			{
				"quantity": -20,
				"value": 30
			}
		))

	# check the holder state. It should show a change in quantity
	# and some profit:
	for subject, state in holder.state.items():
		print(subject)
		print(state)
	# AST1
	# {'value': 20.0, 'quantity': 80}


	# create some other occurrence with that subject.
	# Now a purchase of 10 units of the asset, for the
	# value of $20.
	holder.trade(Occurrence(
			some_asset,
			'2018-01-04',
			{
				"quantity": 10,
				"value": 25
			}
		))

	# check the holder state. It should show a change in quantity
	# and in the value of the subject:
	for subject, state in holder.state.items():
		print(subject)
		print(state)
	# AST1
	# {'value': 20.555555555555557, 'quantity': 90}


License
-------

Copyright (c) 2015-2018 Rafael da Silva Rocha

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
“Software”), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.



.. |Build| image:: https://img.shields.io/travis/rochars/trade.svg?label=unix%20build
   :target: https://travis-ci.org/rochars/trade
.. |Windows Build| image:: https://img.shields.io/appveyor/ci/rochars/trade.svg?label=windows%20build
   :target: https://ci.appveyor.com/project/rochars/trade
.. |Coverage Status| image:: https://coveralls.io/repos/rochars/trade/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/rochars/trade?branch=master
.. |Scrutinizer| image:: https://scrutinizer-ci.com/g/rochars/trade/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/rochars/trade/
.. |Python Versions| image:: https://img.shields.io/pypi/pyversions/trade.png
   :target: https://pypi.python.org/pypi/trade/
.. |Live Demo| image:: https://img.shields.io/badge/try-live%20demo-blue.png
   :target: https://python-trade.appspot.com/
.. |Documentation| image:: https://readthedocs.org/projects/trade/badge/
   :target: http://trade.readthedocs.org/en/latest/
.. |License| image:: https://img.shields.io/pypi/l/trade.png
   :target: https://opensource.org/licenses/MIT
