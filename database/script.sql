CREATE TABLE IF NOT EXISTS log
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    userId   INTEGER NOT NULL,
    username TEXT    NOT NULL,
    message  TEXT    NOT NULL,
    time     TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS questions
(
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS requests_table
(
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    userId      INTEGER NOT NULL,
    username    TEXT    NOT NULL,
    message     TEXT    NOT NULL,
    photo_id    TEXT DEFAULT '',
    video_id    TEXT DEFAULT '',
    time        TEXT    NOT NULL,
    answer      TEXT DEFAULT '',
    answer_time TEXT DEFAULT ''
);