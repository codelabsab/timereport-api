from chalice import Blueprint, AuthResponse
from os import environ
from chalicelib.model.models import EventTable, LockTable
from chalicelib.lib import db_v2


v1_routes = Blueprint(__name__)

api_key = environ["CHALICE_API_KEY"]


@v1_routes.authorizer()
def api_key_auth(auth_request):
    """
    Custom auth function.
    The client need to provide the header Authorization with value of api_key.
    """

    if auth_request.token == api_key:
        return AuthResponse(routes=["/*"], principal_id="user")

    return AuthResponse(routes=[], principal_id="user")


@v1_routes.route("/v1/table-names", cors=True, authorizer=api_key_auth)
def table_names():
    """
    :return: table name
    """
    return {"name": [EventTable.Meta.table_name, LockTable.Meta.table_name]}


@v1_routes.route("/v1/users", methods=["GET"], cors=True, authorizer=api_key_auth)
def list_users():
    """
    Method
    GET    /users
    Return list of all users
    """
    return db_v2.list_users()


@v1_routes.route(
    "/v1/users/{user_id}", methods=["GET"], cors=True, authorizer=api_key_auth
)
def get_user(user_id):
    """
    Method
    GET    /users/<user_id>
    Return a single user
    """
    return db_v2.get_user(user_id)


@v1_routes.route(
    "/v1/users/{user_id}/events", methods=["GET"], cors=True, authorizer=api_key_auth
)
def list_events_by_user_id(user_id):
    """
    Method
    GET    /users/<user_id>/events
    :params from: str, to: str
      filter on date range
    Return a list of all user_id's events
    """
    if v1_routes.current_request.query_params:
        date_from = v1_routes.current_request.query_params.get("from")
        date_to = v1_routes.current_request.query_params.get("to")
        return db_v2.list_events_by_user_id(user_id, date_from, date_to)
    return db_v2.list_events_by_user_id(user_id)


@v1_routes.route(
    "/v1/users/{user_id}/events", methods=["DELETE"], cors=True, authorizer=api_key_auth
)
def delete_all_events_by_user_id(user_id):
    """
    Method
    DELETE    /users/<user_id>/events
    Delete all the user_id's events
    """
    return db_v2.delete_all_events_by_user_id(user_id)


@v1_routes.route(
    "/v1/users/{user_id}/locks", methods=["GET"], cors=True, authorizer=api_key_auth
)
def list_locks_by_user_id(user_id):
    """
    Method
    GET    /users/<user_id>/locks
    Return a list of user_id's locks
    """
    return db_v2.list_locks_by_user_id(user_id)


@v1_routes.route(
    "/v1/users/{user_id}/locks", methods=["DELETE"], cors=True, authorizer=api_key_auth
)
def delete_all_locks_by_user_id(user_id):
    """
    Method
    DELETE    /users/<user_id>/locks
    Delete all locks for user_id
    """
    return db_v2.delete_all_locks_by_user_id(user_id)


@v1_routes.route(
    "/v1/users/{user_id}/locks/{event_date}",
    methods=["DELETE"],
    cors=True,
    authorizer=api_key_auth,
)
def delete_lock_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/locks/<date>
    Delete user_id lock on date
    """
    return db_v2.delete_lock_by_user_id_and_date(user_id, event_date)


@v1_routes.route(
    "/v1/users/{user_id}/events/{event_date}",
    methods=["DELETE"],
    cors=True,
    authorizer=api_key_auth,
)
def delete_event_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/events/<date>
    Delete user_id's event on date
    """
    return db_v2.delete_event_by_user_id_and_date(user_id, event_date)


@v1_routes.route(
    "/v1/users/{user_id}/events/{event_date}",
    methods=["GET"],
    cors=True,
    authorizer=api_key_auth,
)
def get_event_by_user_id_and_date(user_id, event_date):
    """
    Method
    DELETE    /users/<user_id>/events/<date>
    Delete user_id's event on date
    """
    return db_v2.get_event_by_user_id_and_date(user_id, event_date)


@v1_routes.route("/v1/events", methods=["POST"], cors=True, authorizer=api_key_auth)
def create_event_v2():
    """
    Method
    POST    /events
    Create event
    data: {"user_id":"foo01","user_name":"Foo Bar","reason":"sick","event_date":"2019-03-21","hours":8} OR list with same format data
    """
    return db_v2.create_event_v2(v1_routes.current_request.json_body)


@v1_routes.route("/v1/events", methods=["GET"], cors=True, authorizer=api_key_auth)
def list_all_events():
    """
    Method
    GET    /events
    Returns list of all events
    """
    return db_v2.list_all_events()


@v1_routes.route(
    "/v1/events/dates/{event_date}", methods=["GET"], cors=True, authorizer=api_key_auth
)
def list_all_events_by_date(event_date):
    """
    Method
    GET    /events/dates/<date>
    Returns list of all events on date
    """
    return db_v2.list_all_events_by_date(event_date)


@v1_routes.route(
    "/v1/events/dates/{event_date}",
    methods=["DELETE"],
    cors=True,
    authorizer=api_key_auth,
)
def delete_all_events_by_date(event_date):
    """
    Method
    DELETE    /events/dates/<date>
    Delete all events on date
    """
    return db_v2.delete_all_events_by_date(event_date)


@v1_routes.route("/v1/locks", methods=["POST"], cors=True, authorizer=api_key_auth)
def create_lock():
    """
    Method
    POST    /locks
    Create lock
    data: {"user_id":"foo01","event_date":"2019-02"}
    """
    db_v2.create_lock(v1_routes.current_request.json_body)
    return v1_routes.current_request.json_body


@v1_routes.route("/v1/locks", methods=["GET"], cors=True, authorizer=api_key_auth)
def list_all_locks():
    """
    Method
    GET    /locks
    Returns list of all locks
    """
    return db_v2.list_all_locks()


@v1_routes.route(
    "/v1/locks/dates/{event_date}", methods=["GET"], cors=True, authorizer=api_key_auth
)
def list_all_locks_by_date(event_date):
    """
    Method
    GET    /locks/dates/<date>
    Returns list of all locks on date
    """
    return db_v2.list_all_locks_by_date(event_date)


@v1_routes.route(
    "/v1/locks/dates/{event_date}",
    methods=["DELETE"],
    cors=True,
    authorizer=api_key_auth,
)
def delete_all_locks_by_date(event_date):
    """
    Method
    DELETE    /locks/dates/<date>
    Delete all locks on date
    """
    return db_v2.delete_all_locks_by_date(event_date)

