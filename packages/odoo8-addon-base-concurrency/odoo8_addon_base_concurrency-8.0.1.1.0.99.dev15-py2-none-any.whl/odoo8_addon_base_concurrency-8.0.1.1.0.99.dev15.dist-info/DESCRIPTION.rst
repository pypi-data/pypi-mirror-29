Module to regroup all workarounds/fixes to avoid concurrency issues in SQL.

* res.users login_date:
the login date is now separated from res.users; on long transactions,
"re-logging" by opening a new tab changes the current res.user row,
which creates concurrency issues with PostgreSQL in the first transaction.

This creates a new table and a function field to avoid this. In order to
avoid breaking modules which access via SQL the login_date column, a cron
(inactive by default) can be used to sync data.


