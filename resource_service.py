import json, falcon, jwt, base64


jwt_public_key = None


class GenericResource:
    def on_get(self, request, response):
        if not 'AUTHORIZATION' in request.headers:
            response.status = falcon.HTTP_401
            return

        auth_header = request.headers['AUTHORIZATION']
        auth_header_prefix = 'bearer '
        if not auth_header.lower().startswith(auth_header_prefix):
            response.status = falcon.HTTP_401
            return
        token_base64 = auth_header[len(auth_header_prefix):]

        token = base64.b64decode(token_base64).decode('utf-8')
        public_claims = jwt.decode(token, jwt_public_key, algorithms='RS256')

        response.body = json.dumps(public_claims)
        response.status = falcon.HTTP_200


with open('jwt_key.pub') as jwt_public_key_file:
    jwt_public_key = jwt_public_key_file.read()

api = falcon.API()
api.add_route('/', GenericResource())
