Spinach
=======

.. image:: https://travis-ci.org/NicolasLM/spinach.svg?branch=master
    :target: https://travis-ci.org/NicolasLM/spinach
.. image:: https://coveralls.io/repos/github/NicolasLM/spinach/badge.svg?branch=master
    :target: https://coveralls.io/github/NicolasLM/spinach?branch=master
.. image:: https://readthedocs.org/projects/spinach/badge/?version=latest
    :target: http://spinach.readthedocs.io/en/latest/?badge=latest

Redis task queue for Python 3 heavily inspired by Celery and RQ.

Distinctive features:

- Threads first, workers are lightweight
- Explicit, very little black magic that can bite you
- Modern code in Python 3 and Lua
- Workers are embeddable in regular processes for easy testing
- See `Design choices
  <https://spinach.readthedocs.io/en/latest/user/design.html>`_ for more
  details

Quickstart
----------

Install Spinach with pip::

   pip install spinach

Create task and schedule two jobs, one executed now and one later:

.. code:: python

    from spinach import Engine, MemoryBroker

    spin = Engine(MemoryBroker())


    @spin.task(name='compute')
    def compute(a, b):
        print('Computed {} + {} = {}'.format(a, b, a + b))


    # Schedule a job to be executed ASAP
    spin.schedule('compute', 5, 3)

    print('Starting workers, ^C to quit')
    spin.start_workers()

Documentation
-------------

The documentation is at `https://spinach.readthedocs.io
<https://spinach.readthedocs.io/en/latest/index.html>`_.

License
-------

BSD 2-clause

Copyright (c) 2017, Nicolas Le Manchet
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
   this list of conditions and the following disclaimer in the documentation 
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR 
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


