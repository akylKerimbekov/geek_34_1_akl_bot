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

ALTER_USER_TABLE = """
alter table telegram_users
add column reference_link text
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

CREATE_USER_FORM_TABLE_QUERY = """
    create table if not exists user_forms(
        id integer primary key,
        telegram_id integer,
        nickname char(50),
        bio text,
        age integer,
        occupation char(50),
        photo text,
        unique (telegram_id)
    )
"""

CREATE_LIKE_TABLE_QUERY = """
    create table if not exists like_user(
        id integer primary key,
        owner_telegram_id integer,
        liker_telegram_id integer,
        unique (owner_telegram_id, liker_telegram_id)
    )
"""

CREATE_REFERENCE_TABLE_QUERY = """
    create table if not exists referral(
        id integer primary key,
        owner_telegram_id integer,
        referral_telegram_id integer,
        unique (owner_telegram_id, referral_telegram_id)
    )
"""

INSERT_USER_QUERY = """
    insert or ignore into telegram_users values (?, ?, ?, ?, ?, ?)
"""

UPDATE_USER_REF_QUERY = """
    update telegram_users set reference_link = ? where telegram_id = ?
"""

INSERT_BAN_USER_QUERY = """
    insert into ban_users(id, telegram_id, username, count) values (?, ?, ?, ?)
    on conflict(telegram_id)
    do update set count = count + 1
"""

INSERT_USER_FORM_QUERY = """
    insert into user_forms(id, telegram_id, nickname, bio, age, occupation, photo) values (?, ?, ?, ?, ?, ?, ?)
"""

DELETE_USER_FORM_QUERY = """
    delete from user_forms where telegram_id = ?
"""

UPDATE_USER_FORM_QUERY = """
    update user_forms 
    set nickname = ?, bio = ?, age = ?, occupation = ?, photo = ?
    where telegram_id = ?
"""

SELECT_ALL_USER_QUERY = """
    select * from telegram_users
"""

SELECT_USER_QUERY = """
    select * from telegram_users where telegram_id = ?
"""

SELECT_USER_BY_LINK_QUERY = """
    select * from telegram_users where reference_link = ?
"""

SELECT_USER_FORM_QUERY = """
    select * from user_forms where telegram_id = ?
"""

SELECT_ALL_USER_FORM_QUERY = """
    select * from user_forms
"""

INSERT_LIKE_QUERY = """
    insert into like_user(id, owner_telegram_id, liker_telegram_id) values (?, ?, ?)
"""

INSERT_REFERRAL_QUERY = """
    insert into referral(id, owner_telegram_id, referral_telegram_id) values (?, ?, ?)
"""

SELECT_ALL_REFERRAL_BY_OWNER_QUERY = """
    select * from referral where owner_telegram_id = ?
"""