CREATE_USER_TABLE_QUERY = """
    create table if not exists telegram_users(
        id integer primary key,
        telegram_id integer,
        username char(50),
        first_name char(50),
        last_name char(50),
        unique (telegram_id)
    )
"""

CREATE_BAN_USER_TABLE_QUERY = """
    create table if not exists ban_users(
        id integer primary key,
        telegram_id integer,
        username char(50),
        count integer,
        unique (telegram_id)
    )
"""

INSERT_USER_QUERY = """
    insert or ignore into telegram_users values (?, ?, ?, ?, ?)
"""

INSERT_BAN_USER_QUERY = """
    insert into ban_users(id, telegram_id, username, count) values (?, ?, ?, ?)
    on conflict(telegram_id)
    do update set count = count + 1
"""

SELECT_ALL_USER_QUERY = """
    select * from telegram_users
"""

SELECT_BAN_USER_QUERY = """
    select count from ban_users where telegram_id = ?
"""