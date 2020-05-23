SELECT * FROM forum_threads INNER JOIN (
    SELECT COUNT(*) AS messages_count, COUNT(distinct author) AS users_count, related_to FROM forum_messages GROUP BY related_to LIMIT {} OFFSET {}
) AS threads_data ON threads_data.related_to = forum_threads.id;
