# timereport-api
An API for timereport

## Architecture
* AWS API Gateway
* AWS lambda
* AWS dynamodb

## Setup

- aws credentials for dynamodb access
- aws credentials for travis-ci
- edit .chalice/config.json env variables
- pre-commit

## Event model
```
[
  {
    "reason": "sick",
    "hours": "8",
    "user_name": "Mr User",
    "user_id": "user101",
    "event_date": "2019-03-21"
  }
]
```

## RESTful resources

Resources exposed through the api

Expects `Content-Type: appplication/json`

##### Tables
```
GET    /table-names                   # list dynamo tables
```

##### User context
```
GET    /users                         # list users
GET    /users/<user_id>               # get user
GET    /users/<user_id>/events        # list all user events
DELETE /users/<user_id>/events        # delete all user events
GET    /users/<user_id>/locks         # list all user locks
DELETE /users/<user_id>/locks         # delete all user locks
DELETE /users/<user_id>/locks/<date>  # delete user lock by date
GET    /users/<user_id>/events/<date> # get user event by date
DELETE /users/<user_id>/events/<date> # delete user event by date
```

##### Event context
```
GET    /events                 # list events
POST   /events                 # create event
GET    /events/dates/<date>    # get all events by date
DELETE /events/dates/<date>    # delete all events by date
```

##### Lock context
```
GET    /locks                  # list locks
POST   /locks                  # create lock
GET    /locks/dates/<date>     # list all locks by date
DELETE /locks/dates/<date>     # delete all locks by date
```

## Local development

### Authentication

The API v1 routes requires authentication via the `Authorization` header.

API key is set via `CHALICE_API_KEY` variable in the [Makefile](Makefile).

Example request via `httpie`:
```
# http localhost:8010/v1/table-names 'Authorization: development'
```

### prerequisite
- Docker (to run amazon/dynamodb-local)
- packages in requirements.txt OR `pipenv install`

To start a local dynamodb, setup config and start chalice:
```
$ make config
$ make run
```
Now you should be able to try the API on http://localhost:8010 or run the tests `pipenv run pytest`

To stop and cleanup:
```
make clean
```

## Deployment
Deployment to dev and prod is done automatically via github actions

### DEV
See [dev.yml](.github/workflows/dev.yml) for details.

### PRODUCTION
See [prod.yml](.github/workflows/prod.yml) for details.

### Manually
__note__: This requires that you have setup the credentials for AWS

### DEV
`chalice deploy --stage dev`
### PROD
`chalice deploy --stage prod`

### Run unit tests

#### prerequisite
Install the packages (use pipenv)
```
# make run
# pytest -v tests
```
