==================================================
Redmine to JIRA Importers plugin
==================================================


.. image:: https://img.shields.io/pypi/v/redmine2jira.svg
        :target: https://pypi.python.org/pypi/redmine2jira

.. image:: https://travis-ci.org/wandering-tales/redmine2jira.svg?branch=master
        :target: https://travis-ci.org/wandering-tales/redmine2jira

.. image:: https://readthedocs.org/projects/redmine2jira/badge/?version=latest
        :target: https://redmine2jira.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/wandering-tales/redmine2jira/shield.svg
     :target: https://pyup.io/repos/github/wandering-tales/redmine2jira/
     :alt: Updates

.. image:: https://pyup.io/repos/github/wandering-tales/redmine2jira/python-3-shield.svg
     :target: https://pyup.io/repos/github/wandering-tales/redmine2jira/
     :alt: Python 3

Export Redmine issues to file formats compatible with the JIRA Importers plugin (JIM).

* Free software: MIT license
* Documentation: https://redmine2jira.readthedocs.io.


Features
--------

The aim of the tool is to export Redmine issues, fetched using Redmine REST API,
to a set of files which format is compatible with the JIRA Importers Plugin.

The output of the tool, in most of the scenarios, is a single JSON file
combining all the following information for each exported issue:

- Standard/custom fields
- Journal entries (Notes)
- Status history
- Attachments URLs
- Hierarchy relationships
- Relations
- Watchers
- Time logs

Cross-project issue relations
*****************************

If the Redmine instance has configured cross-project issue relations,
and the exported issues do not correspond to the full set of issues of the
Redmine instance (the tool will properly detect the scenario and prompt a
question if needed), the issue relations will be exported in a separate
CSV file. Subsequently, when all the Redmine issues have been imported
in the target Jira instance that CSV file can be finally imported
in order to update relations on all the existing issues.

JIM file format specifications
******************************

Both the JSON and CSV files produced respectively meet their format specifications
for the JIRA Importers plugin (JIM). Those specifications can be respectively found
in the following KB articles:

- `Cloud / Importing data from JSON <https://confluence.atlassian.com/display/AdminJIRACloud/Importing+data+from+JSON>`_
- `Cloud / Importing data from CSV <https://confluence.atlassian.com/display/AdminJIRACloud/Importing+data+from+CSV>`_
- `Server (latest) / Importing data from JSON <https://confluence.atlassian.com/display/ADMINJIRASERVER/Importing+data+from+JSON>`_
- `Server (latest) / Importing data from CSV <https://confluence.atlassian.com/display/ADMINJIRASERVER/Importing+data+from+CSV>`_

However, it's worth to mention that all the articles, especially the one Related
to JSON format, are more driven by examples rather than being comprehensive
specification documents: several details related both to the structure
and the fields values format are omitted. Sometimes we had the need to rely
on other sources on the Internet to cope some strange scenarios.
Besides, the import from JSON feature is not completely stable.


Prerequisites
-------------

* TODO Users already present in Jira
* TODO Redmine REST API Enabled


Usage
-----

The '--filter' option accept a HTTP GET parameter string.
Here follows the list of the supported filter parameters:

  - issue_id (int or string): Single issue ID or comma-separated issue ID's
  - project_id (int or string): Project ID/identifier
  - subproject_id (int or string): Subproject ID/identifier
    (To be used in conjunction with 'project_id';
     you can use `project_id=X` and `subproject_id=!*`
     to get only the issues of a given project
     and none of its subprojects)
  - tracker_id (int): Tracker ID
  - query_id (int): Query ID
  - status_id (int): ['open', 'closed', '*', id]
    If the filter is not specified the default value will be 'open'.
  - assigned_to_id (int):_Assignee user ID
    (or 'me' to get issues which are assigned to the user
     whose credentials were used to access the Redmine REST API)
  - cf_x: Custom field having ID 'x'.
    The '~' sign can be used before the value to find issues
    containing a string in a custom field.

NB: operators containing ">", "<" or "=" should be hex-encoded so they're parsed correctly. Most evolved API clients will do that for you by default, but for the sake of clarity the following examples have been written with no such magic feature in mind.

To fetch issues for a date range (uncrypted filter is "><2012-03-01|2012-03-07") :
GET /issues.xml?created_on=%3E%3C2012-03-01|2012-03-07

To fetch issues created after a certain date (uncrypted filter is ">=2012-03-01") :
GET /issues.xml?created_on=%3E%3D2012-03-01

Or before a certain date (uncrypted filter is "<= 2012-03-07") :
GET /issues.xml?created_on=%3C%3D2012-03-07

To fetch issues created after a certain timestamp (uncrypted filter is ">=2014-01-02T08:12:32Z") :
GET /issues.xml?created_on=%3E%3D2014-01-02T08:12:32Z

To fetch issues updated after a certain timestamp (uncrypted filter is ">=2014-01-02T08:12:32Z") :
GET /issues.xml?updated_on=%3E%3D2014-01-02T08:12:32Z


Configuration
-------------

* TODO


Versioning
----------

We use `SemVer <http://semver.org/>`_ for versioning.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.10.0 (2018-03-14)
-------------------

New features
************

* Implemented issue journal details export feature
* Implemented issue category list by project feature
* Implemented version list by project feature

Improvements
************

* Added support to version resource type mappings
* Re-engineered definitions of internal domain entities and their mappings via classes and named tuples
* Moved definitions of internal domain entities and their mappings to 'resources' sub-package
* Refactored issues export feature to 'IssueExporter' class
* Improved and optimized description of resource mappings settings
* Slightly improved configuration settings comments
* Updated Sphinx to 1.7.1
* Several code optimizations

Changes
*******

Fixes
*****

* Added Python 2 Unicode compatibility for string type
* Used project identifier instead of its internal ID to fetch per-project static resource value mappings
* Used lists instead of sets to achieve Json format serializer compatibility
* Used safer method to check for journal notes existence before fetching them


0.9.0 (2018-02-11)
------------------

Improvements
************

* Update coverage from 4.5 to 4.5.1

Changes
*******

* Disable possibility to skip dynamic value mapping feature
* Remove printing of issues referenced users at the end of export phase.

  As both static and dynamic value mappings are enabled for user resources,
  the final user doesn't need to be warned for something he consciously did in either case.

Fixes
*****

* Honor value mappings for user resources


0.8.0 (2018-02-10)
------------------

New features
************

* Implemented issue watchers save method
* Implemented issue attachments save method
* Partially implemented issue journals save method. Redmine journal notes are saved to Jira comments.

Fixes
*****

* Apply conversion to Confluence Wiki notation only if Textile or Markdown text formatting is enabled in settings


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


