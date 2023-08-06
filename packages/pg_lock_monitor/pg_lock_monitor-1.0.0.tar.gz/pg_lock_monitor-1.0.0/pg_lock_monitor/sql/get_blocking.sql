SELECT pid,
       backend_start,
       xact_start,
       query_start,
       query,
       state,
       cardinality(pg_blocking_pids(pid)) > 0 AS is_blocked,
       pg_blocking_pids(pid) AS blockers,

  (SELECT array_agg(ROW(MODE, relation::regclass))
   FROM pg_locks
   WHERE pg_locks.pid = pg_stat_activity.pid) AS locks
FROM pg_stat_activity
WHERE pid = ANY (%s)