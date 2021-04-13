from chalice import Blueprint, AuthResponse
from os import environ


v1_routes = Blueprint(__name__)

api_key = environ.get("CHALICE_API_KEY", "development")


@v1_routes.authorizer()
def api_key_auth(auth_request):
    """
    Custom auth function.
    The client need to provide the header Authorization with value of api_key.
    """

    if auth_request.token == api_key:
        return AuthResponse(routes=["/*"], principal_id="user")

    return AuthResponse(routes=[], principal_id="user")


@v1_routes.route("/v1/foo", authorizer=api_key_auth)
def foo():
    return {"foo": "bar"}

