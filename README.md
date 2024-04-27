## Bugs in the assignment

* `assignment.md` states "Once you have managed to create the tables, you can find a dump in the data folder to populate it." However, there was no code snippet to do so. Hence I defined SQL scripts to create the tables and dump the values.

* organisation_id 50 not defined:
  ```
  psql:docker-entrypoint-initdb.d/dump_scripts/bikes.sql:1395: ERROR:  insert or update on table "bikes" violates foreign key constraint "bikes_organisation_id_fkey"
  DETAIL:  Key (organisation_id)=(50) is not present in table "organisations".
  ```