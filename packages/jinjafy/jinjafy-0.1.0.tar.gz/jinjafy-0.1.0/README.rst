=======
jinjafy
=======
Render a `Jinja2 <http://jinja.pocoo.org/>`_ template from the commandline, writing it to stdout.

Install
-------
Run ``pip install jinjafy`` to install the ``jinjafy`` command line tool.


Usage
--------
::

    $ jinjafy --help
    usage: jinjafy [-h] [-v] filepath [key=value [key=value ...]]
    ...

    $ cat ru.j2
    Ben De La {{creme}}, {{allstar}}

    $ jinjafy ru.j2 creme=Christ allstar="All Star"
    Ben De La Christ, All Start

Development
-----------
This project uses [`Pipenv`](docs.pipenv.org) to isolate development environments. To test::

    $ pipenv shell
    pytest


License
-------
`MIT <LICENSE>`_
