# basic-jwt-wsgi

Demo service that serves a JWT Bearer token in response to a Basic Auth request.

## About

The goal here is to learn a bit more about Python, [WSGI](https://www.python.org/dev/peps/pep-3333/), [Basic Auth](https://tools.ietf.org/html/rfc7617), and [JWT](https://jwt.io/).

Although I will be making attempts to create a quality solution demonstrating some good practices, be reminded that this project is provided *without warranty* and is meant only as a hobby project. Do not deploy this to production or use it in critical systems.

## Take-Aways

Some stuff I learned from working on this demo.

* `/docker-entrypoint-initdb.d` is a folder you can add to Docker images for first-run database initialization scripts

Python 3 with pipenv is required. The dependency libpq is needed to install psycopg2.

* `apt-get install libpq-dev`
* `pipenv install`

### Postgres 11

TODO: this whole section should be replaced with building a Postgres-Alpine base image Docker container with schema init scripts, so that spinning up the db is a minimal effort

If you don't already have Postgres installed, you'll need [to do that](https://www.postgresql.org/download/linux/ubuntu/) (unless you go the MongoDB route but I haven't added that yet.)

You may want to spin up Postgres using Docker (see below), but be skeptical of running databases in containers. Containers are generally meant to come and go, and having your database instance suddenly get wiped out may result in data loss if you don't understand how Docker is managing your data files.

* `docker run -p 5432:5432 --name basic_jwt_postgres -e POSTGRES_PASSWORD=adminpass postgres:alpine`
* `psql -h localhost -p 5432 -U postgres -f user_credentials.sql`

### User Credentials

A script is provided for populating the database with some user credentials to try.

* `python3 add_user.py my_user my_pass`

### Grant Service

Launch the service:

* `gunicorn grant_service:api`

Try a request:

* `curl localhost:8000`

It is convenient to use a tool like Postman for the Basic Auth header.



* TODO: creating the SSL certificate
* TODO: creating the services, Docker containers
* TODO: launching it all
* TODO: test requests

## Architecture

Two services are provided: a grant service and a resource service. Requests must be SSH secured; a [self-signed certificate](https://en.wikipedia.org/wiki/Self-signed_certificate) is good enough for demo purposes. The JWT token itself will be signed using an assymetric RSA pair as well, so that (in theory) the identity of the grant service is well established.

The grant service accepts Basic Auth GET requests and responds with a JWT on success. It reads credentials and JWT contents from a data store.

The resource service accepts JWT requests and responds with 202 Accepted only if the token is present and valid. This demonstrates the idea of [federated identity](https://en.wikipedia.org/wiki/Federated_identity) in a simple way.

## Data Schema

A table with username, password, and JWT grants is assumed. The passwords must be [salted](https://en.wikipedia.org/wiki/Salt_(cryptography)) and hashed.

Setup instructions for Postgres will be provided, and Mongo if I feel like it.

## Tech Stack

* Nginx as a reverse proxy
* [Falcon](https://falconframework.org/) + [Gunicorn](https://gunicorn.org/) to start
  * Bjoern may be faster but probably harder to set up, consider it a stretch goal
* [PyJWT](https://pyjwt.readthedocs.io/en/latest/) for token processing
* [psycopg2](https://www.psycopg.org/) for Postgres connection
* Docker with Alpine base images to wrap the services

## Cheatsheet

### Docker

The `docker run` command is only used on first creating the container. You need more Docker-fu to manage existing containers. Exiting a running container doesn't delete it, merely stops it.

* `docker ps -a`
* `docker start basic_jwt_postgres`
* `docker stop basic_jwt_postgres`
* `docker rm basic_jwt_postgres`

### Postgres

* `psql -h localhost -p 5432 -U username -f script_to_run.sql`

## References

* [Simple Http Auth example by Bernardas Ališauskas](https://github.com/Granitosaurus/sauth/blob/master/sauth.py)
* [Python 3 Hashlib](https://docs.python.org/3/library/hashlib.html)
* [BLAKE2](https://blake2.net/)
* [Basic Usages of Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html)
* [Docker Run](https://docs.docker.com/engine/reference/commandline/run/)
* [Connect From Your Local Machine to a PostgreSQL Docker Container](https://medium.com/better-programming/connect-from-local-machine-to-postgresql-docker-container-f785f00461a7)
