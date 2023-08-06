CorpusSearch
============

A tool to load and search in text corpora.

The tool provides routines to search in large corpora in pandas
dataframe format, where rows contain textual information on the level of
sentences or paragraphs. Dataframes can be single or multilevel indexed
and loaded from url, doi or local files. Accepted formats are pickle,
excel, json and csv.

This package is designed to work with Jupyter Notebooks as well as in
the IPython command line. If used in a Notebook, the search can be done
through a GUI.

Installation
============

The package can be installed via ``pip``:

::

      pip install corpussearch

Since the package is under active development, the most recent version
is always on Github, and can be installed by

::

      pip install git+https://github.com/TOPOI-DH/corpussearch.git

Basic usage
===========

Import the package

.. code:: python

    from corpussearch.base import CorpusTextSearch

The class is instantiated by providing the path to the source file.
Excepted formats are pickled dataframes, CSV, JSON or Excel files.

Standard parameters assume pickled, multi-indexed dataframes, where the
main text is contained in a column 'text'. For other sources change
parameters accordingly.

.. code:: python

      search = CorpusTextSearch('./path/to/dataframe/file.pickle')

A reduction to a specific part and page number is obtained by chaining
the desired reductions ``.reduce(key,value)``, where ``key`` can be
either a level of the multi index, or a column name. To obtain the
resulting dataframe, ``.results()`` is added.

.. code:: python

      result = search.reduce('part','part_name').reduce('page','page_number').results()

GUI usage
=========

**Attention:** *Work in progress*

Import the GUI part of the package into a Jupyter Notebook

.. code:: python

    from corpussearch.gui import CorpusGUI

Instantiate with path to source file, as above.

.. code:: python

      gui = CorpusGUI('./path/to/dataframe/file.pickle')

and display the interface

.. code:: python

      gui.displayGUI()

A basic word search returns all results where the search word is
contained in the main column, e.g. 'text'. Search values can contain
regular expressions, e.g. ``\d{2,4}\s[A-Z]``. For search in parts other
then the main column, fuzzy searches are possible if the number of
unique values on that level is less than ``maxValues``. This routine
uses ``difflib`` to compare the search string to possible values on that
level. This can help if the actual string formating is not well known,
but could possibly lead to undesired results.

Results are displayed in the sentence output boxes, where the right box
contains meta-information derived from the non-main columns or
multi-index levels.

To navigate between results use the 'previous' and 'next' buttons.

Additional search logic
-----------------------

To chain search terms, use the 'more'-button. This opens additional
search fields. Possible logic operations are 'AND', 'OR', and 'NOT'.
Each logic operation is between two consecutive search pairs
(part,value). The logic operates in a linear fashion, from the first
triple downwards, e.g. for the search (('text','NAME') &
('part','PART1') \| ('page','PAGE4')) each tuple (key,value) yields a
boolean vector v, such that the search becomes (v1 & v2 \| v3).
Evaluation continues for the pair vtemp = (v1 & v2), and finally vres=
(vtemp \| v3). The resulting boolean vector is used to reduce the full
data to the dataframe containing the search result.


