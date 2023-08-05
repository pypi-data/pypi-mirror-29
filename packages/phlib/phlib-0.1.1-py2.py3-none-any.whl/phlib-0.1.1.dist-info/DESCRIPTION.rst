
phlib: empowering… porn?
========================

This is a simple library that scrapes PornHub for content, and provides
a simple, elegant API for interacting with the website.

Only Python 3 is supported.

Example Usage
-------------

::

    >>> from phlib import PornHub
    >>> ph = PornHub()

    >>> ph.categories
    ...

    >>> ph['example category']
    <Category title='example category'>

    >>> cat = _
    >>> cat.videos(max=25)
    ...

    >>> ph.search('some search term')
    ...

Videos have a ``download()`` method, which will download the
video to your current directory.

A CLI utility is provided, ``ph``::

    Ph — empowering porn users everywhere.

    Usage:
      ph <search>... [--max=<n>] [--meta] [--download]
      ph (-h | --help)
      ph --version

    Options:
      -h --help     Show this screen.
      --version     Show version.
      --max=<n>     Maximum number of videos to list [default: 25].
      --meta        Display video meta-data.
      --list        List categories.
      --download    Downloads videos.

Enjoy!


