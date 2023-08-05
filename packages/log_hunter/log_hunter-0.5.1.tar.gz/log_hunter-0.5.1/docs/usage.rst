=====
Usage
=====

General Remarks
---------------

The goal of *log_hunter* is to give *easy* access to the data, not *flexible*
access. There is always a compromise between ease of use and flexibility.

The excellent *elasticsearch-dsl* python library on pypi which is used under
the hood offers all the flexibility you need and it would not be productive
to replicate this with a wrapper. If you need that flexibility, that would be my
recommendation.

That being said, often you can get what you want easier and faster by following
a *stepwise refinement* process.

1. Filter the data roughly to have workable data set
2. Filter the results in your code to refine the results
3. Process and transform your results in information

I see *log_hunter* only as playing a role in step 1 : reducing the data to
manageable size and then start filtering, mapping, and reducing the results
to information in steps 2 and 3 in code.


Command Line
------------

the command line tool will show the recognized options when ran with the
*--help* option :

.. code-block::

    $ log_hunter --help
    Usage: log_hunter [OPTIONS] [TERM]

    Options:
      -i, --image TEXT   match lines on a specific docker image name
      -a, --after TEXT   limit to loglines after a certain time in ES syntax
      -b, --before TEXT  limit to loglines before a certain time in ES syntax
      -e, --env TEXT     limit to loglines from either test, uat or prod
                         environments
      --help             Show this message and exit.



From Python Code or Jupyter Notebook
------------------------------------

To use Hunter Log File Access in a project:

.. code-block:: python

    from log_hunter import log_hunter

    results = log_hunter.match_message_results(None, image="absences")

will return all the loglines from images with *absences* as part of the name over the last hour.

here is a result on the python console :

.. code-block:: python

    >>> from log_hunter import log_hunter
    >>> results = log_hunter.match_message_results('updating', image='absences', after='now-1d')
    >>> print(len(results))
    3475

Similarly here is a sample how to use it in a *Jupyter Notebook* :

.. image:: sample_notebook.png

