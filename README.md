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

1. Set the env variable `DB_HOST` to `http://localhost:8000`
2. Create config and start chalice
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
