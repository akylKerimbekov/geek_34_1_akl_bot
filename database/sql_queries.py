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

CREATE_RESULT_TABLE_QUERY = """
    create table if not exists questionnaire_result(
        id integer primary key,
        telegram_id integer,
        result char(50),
        created timestamp default current_timestamp
    )
"""

INSERT_USER_QUERY = """
    insert or ignore into telegram_users values (?, ?, ?, ?, ?)
"""

INSERT_RESULT_QUERY = """
    insert or ignore into questionnaire_result(id, telegram_id, result) values (?, ?, ?)
"""

SELECT_RESULT_QUERY = """
    select * from questionnaire_result
"""
