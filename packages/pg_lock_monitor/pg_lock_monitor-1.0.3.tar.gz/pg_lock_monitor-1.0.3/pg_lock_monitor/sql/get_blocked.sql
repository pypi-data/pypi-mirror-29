SELECT pid,
       backend_start,
       xact_start,
       state_change,
       query_start,
       query,
       pg_blocking_pids(pid) AS blocked_by,
       wait_event_type,
       wait_event,

  (SELECT pg_locks.mode
   FROM pg_locks
   WHERE pg_locks.pid = pg_stat_activity.pid
     AND pg_locks.locktype = pg_stat_activity.wait_event
   LIMIT 1) AS lock_mode
FROM pg_stat_activity
WHERE cardinality(pg_blocking_pids(pid)) > 0;