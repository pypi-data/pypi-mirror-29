.. image:: https://travis-ci.org/ndanielsen/py-opensecrets.svg?branch=master
    :target: https://travis-ci.org/ndanielsen/py-opensecrets

.. image:: https://coveralls.io/repos/github/ndanielsen/py-opensecrets/badge.svg
:target: https://coveralls.io/github/ndanielsen/py-opensecrets


Py-OpenSecrets API
===================

An unofficial Python client for the `Center for Responsive Politics API <https://www.opensecrets.org/resources/create/apis.php>` at OpenSecrets.org.

Access campaign contribution and personal financial data for US congressional members.

You will need a `Center for Responsive Politics API key <https://www.opensecrets.org/api/admin/index.php?function=signup>`.

Forked and built upon from:

https://github.com/robrem/opensecrets-crpapi
https://github.com/opensecrets/python-crpapi

Goal
-------

Add higher test coverage and more utilities to enable better and more efficient use
of the Open Secrets API.

Install
-------

From PyPI:

::
    pip install py-opensecrets


Or, download and use the install script:

::

    git clone https://github.com/ndanielsen/py-opensecrets && cd py-opensecrets
    python setup.py install

Usage
-----

All API functions are abstracted to corresponding client methods, and accept the respective parameters. Results are returned in JSON format, and pre-parsed to trim the fat. For example:

::

    >>> from opensecrets import CRP
    >>> crp = CRP(API_KEY)

    # get a specific legislator by CID
    >>> cand = crp.candidates.get('N00007360')
    >>> cand['lastname']
    'PELOSI'

    # get the top contributors to a candidate for a specific cycle
    >>> contribs = crp.candidates.contrib('N00007360', '2016')
    >>> contribs[0]['@attributes']['org_name']
    'ActBlue'

    # get fundraising information for a committee's members, by industry
    >>> cmte = crp.committees.cmte_by_ind('HARM', 'F10')
    >>> cmte[0]['@attributes']['member_name']
    'Heck, Joe'

    # use fetch to access the endpoints more directly, without pre-parsed results
    >>> summ = crp.fetch('candSummary', cid='N00007360')
    >>> summ['summary']['@attributes']['first_elected']
    '1987'

Contributing
-----

Please read CONTRIBUTING.md
