
This plugin for `PieCrust`_ lets you use `Hoedown Markdown`_ via `Misaka`_ for
faster Markdown processing. It's much faster than the default pure Python (but
more universal) Markdown formatter that comes by default with PieCrust.

To install the plugin::

    pip install piecrust-hoedown

Then enable it in your website configuration::

    site:
      plugins: [hoedown]

You can specifically use the Hoedown formatter on a per-page basis by adding
``format: hoedown`` in the page's configuration header, but you might want to
just make it the default formatter for the whole website::

    site:
      default_format: hoedown
      auto_formats:
        md: hoedown

The Hoedown formatter should be mostly compatible with the default Markdown
formatter, in the sense that making it the default formatter as specified above
should just work, and would make the website bake faster. However, if you were
using Markdown Extensions, there may or may not be any equivalent in Hoedown.
In this case, your best bet is to replace ``markdown`` with ``hoedown`` when
declaring the extensions, and see if there's an error about an extension not
existing. For instance::

    site:
      default_format: hoedown
    hoedown:
      extensions: [fenced_code, footnotes, smarty]

The list of `extensions`_ is available on the Misaka documentation. Any
extension with a dash can also be written with an underscore.

.. _piecrust: http://bolt80.com/piecrust/
.. _hoedown markdown: https://github.com/hoedown/hoedown
.. _misaka: http://misaka.61924.nl/
.. _extensions: http://misaka.61924.nl/#extensions


