# basic-jwt-wsgi

Demo service that serves a JWT Bearer token in response to a Basic Auth request.

## About

The goal here is to learn a bit more about Python, [WSGI](https://www.python.org/dev/peps/pep-3333/), [Basic Auth](https://tools.ietf.org/html/rfc7617), and [JWT](https://jwt.io/).

Although I will be making attempts to create a quality solution demonstrating some good practices, be reminded that this project is provided *without warranty* and is meant only as a hobby project. Do not deploy this to production or use it in critical systems.

## Setup

TODO: creating the database
TODO: creating the SSL certificate
TODO: creating the services, Docker containers
TODO: launching it all
TODO: test requests

## Architecture

Two services are provided: a grant service and a resource service. Requests must be SSH secured; a [self-signed certificate](https://en.wikipedia.org/wiki/Self-signed_certificate) is good enough for demo purposes. The JWT token itself will be signed using an assymetric RSA pair as well, so that (in theory) the identity of the grant service is well established.

The grant service accepts Basic Auth requests and responds with a JWT on success. It reads credentials and JWT contents from a data store.

The resource service accepts JWT requests and responds with 202 Accepted only if the token is present and valid. This demonstrates the idea of [federated identity](https://en.wikipedia.org/wiki/Federated_identity) in a simple way.

## Data Schema

A table with username, password, and JWT grants is assumed. The passwords must be [salted](https://en.wikipedia.org/wiki/Salt_(cryptography)) and hashed, for which a cli tool is provided.

Setup instructions for Postgres will be provided, and Mongo if I feel like it.

## Tech Stack

* Nginx as a reverse proxy
* [Falcon](https://falconframework.org/) + [Gunicorn](https://gunicorn.org/) to start
** Bjoern may be faster but probably harder to set up, consider it a stretch goal
* [PyJWT](https://pyjwt.readthedocs.io/en/latest/) for token processing
* Docker with Alpine base images to wrap the services

## References

* [Simple Http Auth example by Bernardas Ališauskas](https://github.com/Granitosaurus/sauth/blob/master/sauth.py)
* [Basic Usages of Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html)
