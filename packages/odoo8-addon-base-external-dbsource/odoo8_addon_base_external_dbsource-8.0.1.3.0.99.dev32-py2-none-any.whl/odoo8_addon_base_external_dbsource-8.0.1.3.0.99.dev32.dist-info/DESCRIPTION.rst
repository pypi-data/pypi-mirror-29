This module allows you to define connections to foreign databases using ODBC,
Oracle Client or SQLAlchemy.

Database sources can be configured in Settings > Configuration -> Data sources.

Depending on the database, you need:
 * to install unixodbc and python-pyodbc packages to use ODBC connections.
 * to install FreeTDS driver (tdsodbc package) and configure it through ODBC to
   connect to Microsoft SQL Server.
 * to install and configure Oracle Instant Client and cx_Oracle python library
   to connect to Oracle.

Contributors
============

* Maxime Chambreuil <maxime.chambreuil@savoirfairelinux.com>


