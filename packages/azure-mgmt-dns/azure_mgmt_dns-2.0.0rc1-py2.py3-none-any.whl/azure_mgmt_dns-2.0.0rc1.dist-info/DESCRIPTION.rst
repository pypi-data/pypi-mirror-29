Microsoft Azure SDK for Python
==============================

This is the Microsoft Azure DNS Management Client Library.

Azure Resource Manager (ARM) is the next generation of management APIs that
replace the old Azure Service Management (ASM).

This package has been tested with Python 2.7, 3.4, 3.5 and 3.6.

For the older Azure Service Management (ASM) libraries, see
`azure-servicemanagement-legacy <https://pypi.python.org/pypi/azure-servicemanagement-legacy>`__ library.

For a more complete set of Azure libraries, see the `azure <https://pypi.python.org/pypi/azure>`__ bundle package.


Compatibility
=============

**IMPORTANT**: If you have an earlier version of the azure package
(version < 1.0), you should uninstall it before installing this package.

You can check the version using pip:

.. code:: shell

    pip freeze

If you see azure==0.11.0 (or any version below 1.0), uninstall it first:

.. code:: shell

    pip uninstall azure


Usage
=====

For code examples, see `DNS Management
<https://docs.microsoft.com/python/api/overview/azure/dns>`__
on docs.microsoft.com.


Provide Feedback
================

If you encounter any bugs or have suggestions, please file an issue in the
`Issues <https://github.com/Azure/azure-sdk-for-python/issues>`__
section of the project.


.. :changelog:

Release History
===============

2.0.0rc1 (2018-03-14)
+++++++++++++++++++++

**Features**

- Add public/private zone
- Add record_sets.list_all_by_dns_zone operation
- Add zones.update operation

**Breaking changes**

- 'zone_type' is now required when creating a zone ('Public' is equivalent as previous behavior)

New API version 2018-03-01-preview

1.2.0 (2017-10-26)
++++++++++++++++++

- add record_type CAA
- remove pointless return type of delete

Api version moves from 2016-04-01 to 2017-09-01

1.1.0 (2017-10-10)
++++++++++++++++++

- Add "recordsetnamesuffix" filter parameter to list operations

1.0.1 (2017-04-20)
++++++++++++++++++

This wheel package is now built with the azure wheel extension

1.0.0 (2016-12-12)
++++++++++++++++++

* Initial release


