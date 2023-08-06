Work with the sqlite3 shell
========================
You should normally do this using the ``dbshell`` Django management command, but
if you need to add custom command line arguments or pipe data, take a look a
these examples.

Connect to the database in the sqlite3 shell (same as ``manage.py dbshell``)::

    $ {{backend.sqlite3_cli_command}} {{ dbsettings.NAME }}

Load a database dump (just like the dbdev_loaddump management command)::

    $ {{backend.sqlite3_cli_command}} {{ dbsettings.NAME }} ".read mydump.sql"

Make a database dump (just like the dbdev_createdump management command)::

    $ {{backend.sqlite3_cli_command}} {{ dbsettings.NAME }} ".dump" > mydump.sql
