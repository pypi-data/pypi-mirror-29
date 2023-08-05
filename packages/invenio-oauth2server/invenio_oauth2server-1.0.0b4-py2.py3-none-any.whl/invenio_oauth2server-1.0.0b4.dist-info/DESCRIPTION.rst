..
    This file is part of Invenio.
    Copyright (C) 2015, 2017 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.

======================
 Invenio-OAuth2Server
======================

.. image:: https://img.shields.io/travis/inveniosoftware/invenio-oauth2server.svg
        :target: https://travis-ci.org/inveniosoftware/invenio-oauth2server

.. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-oauth2server.svg
        :target: https://coveralls.io/r/inveniosoftware/invenio-oauth2server

.. image:: https://img.shields.io/github/tag/inveniosoftware/invenio-oauth2server.svg
        :target: https://github.com/inveniosoftware/invenio-oauth2server/releases

.. image:: https://img.shields.io/pypi/dm/invenio-oauth2server.svg
        :target: https://pypi.python.org/pypi/invenio-oauth2server

.. image:: https://img.shields.io/github/license/inveniosoftware/invenio-oauth2server.svg
        :target: https://github.com/inveniosoftware/invenio-oauth2server/blob/master/LICENSE


Invenio module that implements OAuth 2 server.

* Free software: GPLv2 license
* Documentation: https://invenio-oauth2server.readthedocs.io/

Features
========

* Settings view for configuring applications and personal access tokens.
* Uses encryption field for seamless encryption/decryption of the access
  and refresh tokens.


..
    This file is part of Invenio.
    Copyright (C) 2015, 2016, 2017 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.

Changes
=======

Version 1.0.0b4 (released 2018-02-21)
--------------------------------------

- Refactors package.

Version 0.2.0 (released 2015-10-06)
-----------------------------------

Incompatible changes
~~~~~~~~~~~~~~~~~~~~

- Removes legacy upgrade recipes. You **MUST** upgrade to the latest
  Invenio 2.1 before upgrading Invenio-Upgrader.

Bug fixes
~~~~~~~~~

- Removes calls to PluginManager consider_setuptools_entrypoints()
  removed in PyTest 2.8.0.
- Adds missing `invenio_base` dependency.

Notes
~~~~~

- Disables test_settings_index test case.

Version 0.1.1 (released 2015-08-25)
-----------------------------------

Improved features
~~~~~~~~~~~~~~~~~

- Marks strings in templates for translations.  (#3)

Bug fixes
~~~~~~~~~

- Adds missing `invenio_upgrader` dependency and amends past upgrade
  recipes following its separation into standalone package.

Version 0.1.0 (released 2015-08-04)
-----------------------------------

- Initial public release.


