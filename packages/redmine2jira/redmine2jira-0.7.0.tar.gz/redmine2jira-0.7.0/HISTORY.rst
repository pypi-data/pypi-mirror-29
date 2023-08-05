=======
History
=======

0.7.0 (2018-02-10)
------------------

New features
************

* Implemented issue custom fields save method

Improvements
************

* Used tuples as dictionary keys for both resource type fields mappings and dynamic resource value mappings
* Added comment to explain what happens when no static user-defined mapping has been found and dynamic resource value mapping feature is disabled
* Removed leftovers of old project name "Redmine XLS Export to Jira"

Changes
*******

* Removed 'CUSTOM_' prefix from the resource value mappings setting names

Fixes
*****

* Fixed setting of dynamic resource value mapping when the resource type is defined on a per-project basis
* Removed misleading comment. When a Redmine resource type is mapped to more than one Jira resource type the final user is free to set value mappings across all possible resource type combinations.
* Added default empty dictionary if the resource type mapping setting is not found
* Minor docstring fixes


0.6.2 (2018-02-08)
------------------

Improvements
************

* Add pyenv support for Tox

Fixes
*****
* Fix packages include directive in ``setup.py``


0.6.1 (2018-02-07)
------------------

Fake release to fix a problem in PyPI upload.


0.6.0 (2018-02-07)
------------------

New features
************

* Implemented issue project save method
* Implemented issue standard fields save methods

Improvements
************

* Renamed ``_get_resource_value_mapping`` method to ``_get_resource_mapping``.

  The method now returns both mapped Jira type and value, rather than only value.

  Updated method docstring accordingly.
* Added Redmine general configuration section header

Changes
*******
* Removed Python 3.3 compatibility
* Updated encrypted PyPI password for Travis CI

Fixes
*****

* Replaced references to old ``CUSTOM_USERS_MAPPINGS`` setting with new ``CUSTOM_REDMINE_USER_JIRA_USER_MAPPINGS``
* Retrieved issue user resource instance from cached users list rather than from issue lazy loaded instance
* Disabled dynamic value mapping feature for Redmine "User" resource type


0.5.0 (2018-02-06)
------------------

New features
************

* Added dynamic resource value mapping management at runtime
* Added dynamic resource value mapping for assignee field when it refers to a standard user
* Added command to list issue priorities

Improvements
************

* Made Redmine and Jira respective resource types explicit in the names of settings related to resource value mappings
* Slightly improved settings related comments
* Added labels for values printed in console output
* Improved code readability
* Slightly improved docstrings
* Updated ``sphinx`` to 1.6.7
* Updated ``coverage`` to 4.5


0.4.0 (2018-01-26)
------------------

New features
************

* Added dynamic project mappings management

Improvements
************

* Refactored specific methods to save issue resources
* Minor optimizations


0.3.1 (2018-01-26)
------------------

Improvements
************

* Referenced users and groups are collected on-the-fly while exporting issues. This increases performance.
* Minor enhancements in the console output for the completion of the export

Fixes
*****

* Fix recursive function used in ``list projects`` command to build the full project hierarchical name
* Fixed a bug affecting all the ``list`` commands that caused some resource relations being included in the tables
* Fixed another minor bug affecting all the ``list`` commands


0.3.0 (2018-01-22)
------------------

Improvements
************

* Added early lookup of users and groups references within the issues being exported
* Added command to list Redmine groups
* Added option to list all Redmine users at once, including locked ones
* Enhanced notes in configuration file

Changes
*******

* Added requirements.txt for installation package requirements (useful for pyup.io)


0.2.0 (2018-01-19)
------------------

Improvements
************

* Added PyCharm IDE configuration and Python Virtual Environments to .gitignore
* Added configuration file with defaults and support for local configuration file
* Minor documentation fixes

Changes
*******

* Dropped out "Redmine XLS Plugin" in favor of Redmine REST API.

  Since the files exported by the plugin lack some information needed to produce files compatible with the Jira Importer Plugin (JIM),
  several calls to the Redmine REST API were needed to compensate the data. Hence to avoid the effort to merge the data coming from
  two difference sources I decided to rely solely on Redmine REST API to fetch all the needed data.

  This is a major project scope change that implied, in turn, the following modifications:

  - Renamed GitHub repository from "redmine-xls-export2jira" to "redmine2jira"
  - Renamed Python package from "redmine_xls_export2jira" to "redmine2jira"
  - Rename project description to "Redmine to JIRA Importers plugin"

  Any other reference to the "Redmine XLS Export" plugin has also been removed from the documentation.

* Removed Python 2.7 compatibility. Added Python 3.6 compatibility.
* Temporarily disable CLI tests


0.1.1 (2018-01-05)
------------------

Fixes
*****

* Minor fixes in docs

Improvements
************

* Initial pyup.io update
* Added pyup.io Python 3 badge

Changes
*******

* Linked pyup.io
* Removed CHANGELOG.rst


0.1.0 (2018-01-05)
------------------

* First release on PyPI.
