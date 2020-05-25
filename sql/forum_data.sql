SELECT users.login AS author,
    COALESCE(threads_data.messages_count, 0) AS messages_count,
    COALESCE(threads_data.users_count, 0) AS users_count,
    threads_data.related_to,
    forum_threads.id,
    forum_threads.author as author_id,
    forum_threads.title,
    forum_threads.body,
    forum_threads.date
FROM forum_threads LEFT JOIN (
    SELECT COUNT(*) AS messages_count, COUNT(DISTINCT author) AS users_count, related_to FROM forum_messages
    GROUP BY related_to
) AS threads_data ON threads_data.related_to = forum_threads.id
INNER JOIN users ON users.id = forum_threads.author
ORDER BY forum_threads.date DESC
LIMIT {} OFFSET {};
