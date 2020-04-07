import sys, hashlib, uuid

from psycopg2 import connect, sql

# TODO: fetch db name, username, password from local secrets
# it also needs to be shared by the script that builds the db docker image
db_connection_string = "dbname='postgres' user='postgres' host='localhost' password='adminpass'"


def add_user(db_connection, username, password):
    db_cursor = db_connection.cursor()

    password_salt = uuid.uuid4()
    password_hash = hashlib.blake2b(password.encode('utf-8'), salt=password_salt.bytes)
    grants = '{}'

    query = sql.SQL(
        "INSERT INTO {table} ({fields}) VALUES ({values})")
    query = query.format(
        table = sql.Identifier('user_credentials'),
        fields = sql.SQL(',').join([
            sql.Identifier('username'),
            sql.Identifier('password_hash'),
            sql.Identifier('password_salt'),
            sql.Identifier('grants')]),
        values = sql.SQL(',').join([
            sql.Literal(username),
            sql.Literal(password_hash.hexdigest()),
            sql.Literal(password_salt.hex),
            sql.Literal(grants)]))

    # can debug the query by outputting it like so
    # print(query.as_string(db_cursor))

    db_cursor.execute(query)


if __name__ == '__main__':
    username, password = sys.argv[1:]
    print('adding user', username)

    with connect(db_connection_string) as db_connection:
        add_user(db_connection, username, password)
