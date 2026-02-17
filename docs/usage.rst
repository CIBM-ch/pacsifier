.. _cmdusage:

***********************
Commandline Usage
***********************

`PACSIFIER` is a commandline tool that can be run in a variety of ways, providing a set of command-line interface (CLI) commands, which can be run directly in a shell or via a Docker container, for interacting with a PACS server and manipulating DICOM files.

It consists of the following commands:

* ``pacsifier``: The main command, which can be used to interact with a PACS server and manipulate DICOM files.
* ``pacsifier-anonymize``: Anonymize DICOM files.
* ``pacsifier-create-dicomdir``: Create a DICOMDIR file.
* ``pacsifier-get-pseudonyms``: Get pseudonyms for a list of DICOM files.
* ``pacsifier-move-csv``: Move DICOM files from a PACS server to a local directory.
* ``pacsifier-add-karnak-tags``: Add Karnak tags to DICOM files.
* ``pacsifier-extract-carestream-report``: Extract Carestream reports from DICOM files.

In the following sections, we will describe how to run these commands in a shell and in a Docker container.

Running ``PACSIFIER`` commands in a shell
=========================================

``pacsifier`` command
----------------------

.. argparse::
		:ref: pacsifier.cli.pacsifier.get_parser
		:prog: pacsifier

``pacsifier-anonymize`` command
--------------------------------------

.. argparse::
		:ref: pacsifier.cli.anonymize_dicoms.get_parser
		:prog: pacsifier-anonymize

``pacsifier-create-dicomdir`` command
-------------------------------------

.. argparse::
		:ref: pacsifier.cli.create_dicomdir.get_parser
		:prog: pacsifier-create-dicomdir

``pacsifier-get-pseudonyms`` command
-------------------------------------

.. argparse::
		:ref: pacsifier.cli.get_pseudonyms.get_parser
		:prog: pacsifier-get-pseudonyms

``pacsifier-move-csv`` command
-------------------------------------

.. argparse::
		:ref: pacsifier.cli.move_dumps.get_parser
		:prog: pacsifier-move-csv

``pacsifier-add-karnak-tags`` command
-------------------------------------

.. argparse::
		:ref: pacsifier.cli.add_karnak_tags.get_parser
		:prog: pacsifier-add-karnak-tags

``pacsifier-extract-carestream-report`` command
-----------------------------------------------

.. argparse::
		:ref: pacsifier.cli.extract_carestream_report.get_parser
		:prog: pacsifier-extract-carestream-report


.. _cmdusage-docker:

Running ``PACSIFIER`` commands in Docker
========================================

The Docker image entrypoint runs the provided command in the ``pacsifier_minimal`` conda environment. You can use the Docker wrapper scripts (recommended) or call the CLI commands directly.

Recommended (wrapper scripts)
-----------------------------

.. code-block:: bash

		docker_pacsifier -c config.json -q query.csv -d /output --save

See :ref:`docker_wrappers` for the full list of wrapper scripts and examples.

Direct Docker invocation
------------------------

.. code-block:: bash

		docker run --rm --net=host -v /path/to/my_dir:/base pacsifier:1.0.0 \
			pacsifier --save --info --queryfile /base/my_query.csv --config /base/my_config.json --out_directory /base/my_output_dir
