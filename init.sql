CREATE TABLE IF NOT EXISTS

CREATE TABLE messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  handle TEXT UNIQUE NOT NULL,
  message TEXT NOT NULL
);