===============================
Pipettor Overview
===============================

pipettor - robust, easy to use Python package for running Unix process pipelines

Features
--------

* Creating process pipelines in Python is either complex (e.g. ``subprocess``),
  or not robust (e.g. ``os.system()``).  This package provides aims to address
  these shortcomings.
* Command pipelines are simply specified as a sequence of commands, with each
  command represented as a sequence of arguments.
* Failure of any process in the pipeline results in an exception, with ``stderr``
  included in the exception.
* Pipeline ``stdin/stdout/stderr`` can be passed through from parent process,
  redirected to a file, or read/written by the parent process.
* Asynchronous reading and writing to and from the pipeline maybe done without risk of
  deadlock.
* Pipeline can run asynchronously or block until completion.
* File-like objects for reading or writing a pipeline.
* Documentation: https://pipettor.readthedocs.org.





History
=======

0.3.0 (2018-02-25)
-----------------------
* added open-stying buffering, encoding, and errors options
* source cleanup

0.2.0 (2017-09-19)
-----------------------
* Simplified and log of info and errors levels by removing logLevel options.
* Improvements to documentation.

0.1.3 (2017-06-13)
------------------
* Documentation fixes

0.1.2 (2017-06-11)
------------------
* First public release on PyPI.


