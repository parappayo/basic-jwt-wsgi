import falcon, jwt, base64
from psycopg2 import connect, sql
import basic_auth, password_crypto


# TODO: fetch db name, username, password from local secrets
# it also needs to be shared by the script that builds the db docker image
db_connection_string = "dbname='postgres' user='postgres' host='localhost' password='adminpass'"


jwt_public_key = None


def get_user_credentials(db_connection, username):
    db_cursor = db_connection.cursor()

    query = sql.SQL(
        "SELECT {fields} FROM {table} WHERE username = {username}")
    query = query.format(
        table = sql.Identifier('user_credentials'),
        fields = sql.SQL(',').join([
            sql.Identifier('password_hash'),
            sql.Identifier('password_salt'),
            sql.Identifier('grants')]),
        username = sql.Literal(username));

    db_cursor.execute(query)
    return db_cursor.fetchone()


class GrantResource:
    def on_get(self, request, response):
        if not 'AUTHORIZATION' in request.headers:
            response.status = falcon.HTTP_401
            return

        username, password = basic_auth.decode_header(request.headers['AUTHORIZATION'])
        if username == False:
            response.status = falcon.HTTP_401
            return

        with connect(db_connection_string) as db_connection:
            user_credentials = get_user_credentials(db_connection, username)

            if not user_credentials:
                response.status = falcon.HTTP_403
                return

            password_hash, password_salt, grants = user_credentials
            password_hash = bytes(password_hash)
            password_salt = bytes(password_salt)

            if not password_crypto.validate(password, password_salt, password_hash):
                response.status = falcon.HTTP_403
                return

        token = jwt.encode(grants, jwt_public_key, algorithm='RS256')
        token_base64 = base64.b64encode(token).decode('utf-8')
        response.media = {'token': token_base64}
        response.status = falcon.HTTP_200


with open('jwt_key') as jwt_public_key_file:
    jwt_public_key = jwt_public_key_file.read()

api = falcon.API()
api.add_route('/', GrantResource())
