..
    This file is part of Invenio.
    Copyright (C) 2016, 2017 CERN.

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


API Docs
========

Record Indexer
--------------

.. automodule:: invenio_indexer.api
   :members:


Flask Extension
---------------

.. automodule:: invenio_indexer.ext
   :members:


Celery tasks
------------

.. automodule:: invenio_indexer.tasks
   :members:
.. autotask:: invenio_indexer.tasks.process_bulk_queue(version_type)
.. autotask:: invenio_indexer.tasks.index_record(record_uuid)
.. autotask:: invenio_indexer.tasks.delete_record(record_uuid)


Signals
-------

.. automodule:: invenio_indexer.signals
   :members:
