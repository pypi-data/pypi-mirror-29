# django-pgconninfo

[![travis-ci](https://travis-ci.org/ihabhussein/django-pgconninfo.svg?branch=master)](https://travis-ci.org/ihabhussein/django-pgconninfo)

`django-pgconninfo` picks up PostgreSQL connection configuration from
environment variables and construct a map suitable for assignment to `DATABASES`
in Django settings. This code can handle Heroku, Amazon Elastic Beanstalk,
PostgreSQL service files (`.pg_service.conf`), `libpq` environment variables,
and PostgreSQL password files (`~/.pgpass`).

## Why is it needed

The idea of `pgconninfo` is to avoid hardcoded database location and credentials
in source code. This is desirable for several reasons:

- Credentials don't belong to source code or version control repositories.

- Switching from development to production without code change.

- Major cloud services already adopted environment variables for configuration.

For more on configuration through the environment, check [the twelve-factor
app](https://12factor.net).

## Installation

You can install django-pgconninfo via Pypi:

    pip install django-pgconninfo

## Usage

To use the default engine (psycopg2):

    from pgconninfo import pg_conninfo

    DATABASES = {
        'default': pg_conninfo()
    }

or, to use an alternative engine, explicitly state the engine class:

    from pgconninfo import pg_conninfo

    DATABASES = {
        'default': pg_conninfo('django.contrib.gis.db.backends.postgis')
    }

## Database configuration

`pg_conninfo` can configure the database connection using any of the following
environment variables:

- `DATABASE_URL`

  This is a standard PostgreSQL environment variable and is used by Heroku. The
  format of this variable is described in [PostgreSQL's
  documentation](https://www.postgresql.org/docs/current/static/libpq-connect.html#AEN45527)

- `RDS_HOSTNAME`, `RDS_PORT`, `RDS_DB_NAME`, `RDS_USERNAME`, and `RDS_PASSWORD`

  These are the environment variables used by AWS Elastic Beanstalk and are
  documented in their [developer
  guide](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-rds.html)

- `PGSERVICE`, and optionally `PGSERVICEFILE`

  PostgreSQL's documentation describes the location and format of [connection
  service
  files](https://www.postgresql.org/docs/current/static/libpq-pgservice.html)
  and the [configuration
  keywords](https://www.postgresql.org/docs/current/static/libpq-connect.html#LIBPQ-PARAMKEYWORDS)
  to be used in them

- `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, and `PGPASSWORD`

  The `libpq` environment variables are described in [PostgreSQL's
  documentation](https://www.postgresql.org/docs/current/static/libpq-envars.html)

In addition to environment variables, `pg_conninfo` also checks the  [password
file](https://www.postgresql.org/docs/current/static/libpq-pgpass.html) if no
password was given elsewhere.
