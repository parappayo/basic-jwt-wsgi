import falcon
import basic_auth


class GrantResource:
    def on_get(self, request, response):
        print(request.headers)

        if not 'AUTHORIZATION' in request.headers:
            response.status = falcon.HTTP_401
            return

        auth_header = request.headers['AUTHORIZATION']
        basic_str, auth_key = auth_header.split(' ')
        if not basic_str.lower() == 'basic':
            response.status = falcon.HTTP_401
            return

        username, password = basic_auth.decode(auth_key)

        # TODO: now read from Postgres and validate

        response.body = '{"message": "got here"}'
        response.status = falcon.HTTP_200


api = falcon.API()
api.add_route('/', GrantResource())
