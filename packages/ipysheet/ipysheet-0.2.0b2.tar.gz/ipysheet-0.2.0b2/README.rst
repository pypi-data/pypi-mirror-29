Spreadsheet widget for the Jupyter Notebook
===========================================

``ipysheet`` is a Spreadsheet Jupyter_ widget_ for both the Jupyter notebook and Jupyter lab build using Handsontable_.

Installation using pip:
    #. ``$ pip install ipysheet``

    #. ``$ jupyter nbextension enable --py --sys-prefix ipysheet  # can be skipped for notebook version 5.3 and above``

Installtion for developers:
    $ git clone https://github.com/QuantStack/ipysheet.git
    $ cd ipysheet
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipysheet
    $ jupyter nbextension enable --py --sys-prefix ipysheet  # can be skipped for notebook version 5.3 and above

    

Online documentation:
    http://ipysheet.readthedocs.io/

Source code repository (and issue tracker):
    https://github.com/QuantStack/ipysheet

License:
    MIT -- see the file ``LICENSE`` for details.

.. _Sphinx: http://sphinx-doc.org/
.. _Jupyter: http://jupyter.org/
.. _widget: http://jupyter.org/widgets
.. _Handsontable: https://handsontable.com/
