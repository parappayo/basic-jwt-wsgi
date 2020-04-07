import falcon


class GrantResource:
	def on_get(self, request, response):
		print(request.headers)
		response.body = '{"message": "got here"}'
		response.status = falcon.HTTP_200


api = falcon.API()
api.add_route('/', GrantResource())
