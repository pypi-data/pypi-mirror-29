FirehSQL
========

* URL       : `Github <https://github.com/dozymoe/firehsql/>`_
* License   : GPL v3


Summary
-------

Simple SQL Query Builder, doesn't support CREATE TABLE, field definition and
whatnot, the library only observed the table field names.

Example:


.. code:: python

    from firehsql import SchemaBase

    class UserSchema(SchemaBase):

        TABLE_NAME = 'users'

        FIELDS = ('id', 'username', 'email', 'password', 'is_superuser',
                'is_staff', 'created_at', 'modified_at')

        FILTER_BY_FIELDS = ('id', 'username', 'email', 'created_at')
        ORDER_BY_FIELDS = ('username',)

        # For PostgreSQL to return last inserted id
        RETURNING_FIELDS = ('id',)


.. code:: python

    from itertools import chain
    import psycopg2

    from .schema import UserSchema

    def insert():
        sql = UserSchema.create_insert_sql()
        sql.set_values(
                username='User1',
                password='User1Password',
                email='User1@example.com')

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                # INSERT INTO users (username, password, email)
                #     VALUES (%s, %s, %s)
                #
                # ('User1', 'User1Password', 'User1@example.com')
                cur.execute(str(sql), sql.data)
                
            conn.commit()


    def select():
        sql = UserSchema.create_select_sql()

        filter_ = sql.create_or_filter()
        # The word 'LIKE' will not be checked if it was valid or not,
        # too bothersome, just don't put user's input in there.
        filter_.add(('username', 'Ach%', 'LIKE'))
        filter_.add(('username', 'Abd%', 'LIKE'))
        sql.set_filters(filter_)

        # Assumed DESCENDING if it was prefixed with hyphen (-), the target
        # being http query string.
        sql.set_sorting_order('username', '-id')

        page_size = 10
        page = 1
        page_offset = (page - 1) * page_size
        # Both page_size and page_offset tested to be of type integer.
        sql.set_limit(page_size, page_offset)

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                # SELECT * FROM users WHERE username LIKE %s
                #     OR username LIKE %s ORDER BY username, id DESC
                #     LIMIT 10 OFFSET 0
                #
                # ('Ach%', 'Abd%')
                cur.execute(str(sql), sql.data)


    def update():
        sql = UserSchema.create_update_sql()

        sql.set_values(
                is_superuser=True,
                is_staff=True)

        # '=' will not be checked if it was valid operand or not.
        sql.set_filters(
                ('username', 'User1', '='))

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                # UPDATE users SET is_superuser=%s, is_staff=%s
                #     WHERE username = %s
                #
                # (True, True, 'User1')
                cur.execute(str(sql), sql.data)


    def filter_parser():

        # This is targetted at http query string

        sql = UserSchema.create_select_sql()

        data = {
            'filter_by': {
                'username': 'User%', # starts and/or ends with '%'
                'email': '!null',
                'created_at': '>10-2-2017',
            }
        }

        filters = chain(
            sql.find_filters(data['filter_by'],
                'username', 'email'),

            sql.find_datetime_filters(data['filter_by'],
                'created_at'),
        )

        sql.set_filters(*filters)

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                # SELECT * FROM users WHERE username LIKE %s
                #     AND email IS NOT NULL
                #     AND created_at > %s
                #     LIMIT 10 OFFSET 0
                #
                # ('User%', datetime.datetime(2017, 2, 10, 0, 0, 0, 0,
                #         tzinfo=<UTC>))
                cur.execute(str(sql), sql.data)


    def advance_filter_parser():
        sql = UserSchema.create_select_sql()

        data = {
            'filter_by': [
                'AND',
                [
                    'OR',
                    {'name': 'User%'},
                    {'name': '%User'},
                ],
                [
                    'OR',
                    {'email': '!null'},
                    {'email': '=admin@example.com'},
                },
                {'created_at': '>10-2-2017'},
                {
                    'id': ['=', 1, 2, 3],
                },
                {
                    'id': ['!', 4, 5, 6],
                },
            }
        }

        advanced_filter = sql.parse_adv_filters(
            data['filter_by'],
            (
                ('username', 'name', 'str'),
                ('email', 'str'),
                ('created_at', 'date'),
                ('id', 'int'),
            ))

        sql.set_filters(advanced_filter)

        with psycopg2.connect('dbname=testdb') as conn:
            with conn.cursor() as cur:
                # SELECT * FROM users WHERE
                #     (username LIKE %s OR username LIKE %s)
                #     AND
                #     (email IS NOT NULL OR email = %s)
                #     AND
                #     created_at > %s
                #     AND
                #     id IN (%s, %s, %s)
                #     AND
                #     id NOT IN (%s, %s, %s)
                #     LIMIT 10 OFFSET 0
                #
                # (
                #     'User%', '%User', 'admin@example.com',
                #     datetime(2017, 2, 10, 0, 0, 0, 0, tzinfo=<UTC>),
                #     1, 2, 3, 4, 5, 6,
                # )
                cur.execute(str(sql), sql.data)
