===============================
Gingerit
===============================

.. image:: https://github.com/Azd325/gingerit/workflows/Python%20package/badge.svg

.. image:: https://img.shields.io/pypi/v/gingerit.svg
        :target: https://pypi.python.org/pypi/gingerit


Correcting spelling and grammar mistakes based on the context of complete sentences. Wrapper around the gingersoftware.com API

* Free software: MIT license
* Documentation: https://gingerit.readthedocs.org.

Installation:
-------------

::

    pip install gingerit

Usage:
------

Python
~~~~~~~~

::

    from gingerit.gingerit import GingerIt

    text = 'The smelt of fliwers bring back memories.'

    parser = GingerIt()
    parser.parse(text)

Command Line
~~~~~~~~

::
    $ python gingerit.py [-h] -i INPUT [-o] [-f FILE] [-t {split,truncate}] [-v VERIFY]

  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input text or path to text file
  -o, --output          Print detailed output
  -f FILE, --file FILE  Redirect to output file
  -t {split,truncate}, --truncation {split,truncate}
                        Truncation strategy if the text length exceeds 600 characters
  -v VERIFY, --verify VERIFY

A simple example is as follows:

::
    $ python gingerit.py -i "The smelt of fliwers bring back memories."
    $ The smell of flowers brings back memories.

Thanks
------

Thank you for  `Ginger Proofreader <http://www.gingersoftware.com/>`_ for such awesome service. Hope they will keep it free :)

Thanks to @subosito for this inspriration `Gingerice <https://github.com/subosito/gingerice>`_
