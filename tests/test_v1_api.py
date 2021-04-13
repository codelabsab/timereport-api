import requests
from requests.api import request

local_api = "http://localhost:8010"
local_db = "http://localhost:8000"
testusers = ["testuser1", "testuser2"]
testmonths = ["2019-03", "2019-04"]
event_data = [
    {
        "reason": "sick",
        "hours": "8",
        "user_name": "Test Mctest",
        "user_id": f"{testusers[0]}",
        "event_date": "2019-12-30",
    },
    {
        "reason": "sick",
        "hours": "8",
        "user_name": "Test Mctest",
        "user_id": f"{testusers[0]}",
        "event_date": "2019-12-31",
    },
    {
        "reason": "sick",
        "hours": "8",
        "user_name": "Test Mctest",
        "user_id": f"{testusers[0]}",
        "event_date": "2020-01-01",
    },
]
lock_data = [
    {"user_id": f"{testusers[0]}", "event_date": f"{testmonths[0]}"},
    {"user_id": f"{testusers[0]}", "event_date": f"{testmonths[1]}"},
]
request_session = requests.Session()
request_session.headers = {"Authorization": "development"}

# sanity check to see that we have some certainty that this test will execute
# on local environment
check_local_db = requests.get(f"{local_db}/shell/")
if check_local_db.status_code != 200:
    raise Exception("Local DB check failed")

check_local_api = request_session.get(f"{local_api}/v1/table-names")
if check_local_api.status_code != 200:
    raise Exception("Local API check failed")


def create_event(event: dict):
    r = request_session.post(f"{local_api}/events", json=event)
    return r


def create_lock(lock: dict):
    r = request_session.post(f"{local_api}/locks", json=lock)
    return r


def test_create_event():
    event = event_data[0]
    r = create_event(event)
    assert r.status_code == 200


def test_create_multilpe_events():
    r = create_event(event_data)
    assert r.status_code == 200


def test_create_lock():
    lock = lock_data[0]
    r = create_lock(lock)
    assert r.status_code == 200


def test_list_users():
    r = request_session.get(f"{local_api}/v1/users")
    assert r.status_code == 200


def test_get_user():
    event = event_data[0]
    user_id = event["user_id"]
    create_event(event)
    r = request_session.get(f"{local_api}/v1/users/{user_id}")
    assert r.status_code == 200


def test_list_events_by_user_id():
    event = event_data[0]
    user_id = event["user_id"]
    create_event(event)
    r = request_session.get(f"{local_api}/v1/users/{user_id}/events")
    assert r.status_code == 200


def test_delete_all_events_by_user_id():
    event = event_data[0]
    user_id = event["user_id"]
    create_event(event)
    r = request_session.delete(f"{local_api}/v1/users/{user_id}/events")
    assert r.status_code == 200


def test_list_locks_by_user_id():
    lock = lock_data[0]
    user_id = lock["user_id"]
    create_lock(lock)
    r = request_session.get(f"{local_api}/v1/users/{user_id}/locks")
    assert r.status_code == 200


def test_delete_all_locks_by_user_id():
    lock = lock_data[0]
    user_id = lock["user_id"]
    create_lock(lock)
    r = request_session.delete(f"{local_api}/v1/users/{user_id}/locks")
    assert r.status_code == 200


def test_delete_lock_by_user_id_and_date():
    lock = lock_data[0]
    user_id = lock["user_id"]
    date = lock["event_date"]
    create_lock(lock)
    r = request_session.delete(f"{local_api}/v1/users/{user_id}/locks/{date}")
    assert r.status_code == 200


def test_get_event_by_user_id_and_date():
    event = event_data[0]
    user_id = event["user_id"]
    create_event(event)

    event = event_data[1]
    create_event(event)

    r = request_session.get(f"{local_api}/v1/users/{user_id}/events/")
    assert r.status_code == 200


def test_delete_event_by_user_id_and_date():
    event = event_data[0]
    user_id = event["user_id"]
    date = event["event_date"]
    create_event(event)
    r = request_session.delete(f"{local_api}/v1/users/{user_id}/events/{date}")
    assert r.status_code == 200


def test_list_all_events():
    event = event_data[0]
    create_event(event)
    r = request_session.get(f"{local_api}/v1/events")
    assert r.status_code == 200


def test_list_all_events_by_date():
    event = event_data[0]
    date = event["event_date"]
    create_event(event)
    r = request_session.get(f"{local_api}/v1/events/dates/{date}")
    assert r.status_code == 200


def test_delete_all_events_by_date():
    event = event_data[0]
    date = event["event_date"]
    create_event(event)
    r = request_session.delete(f"{local_api}/v1/events/dates/{date}")
    assert r.status_code == 200


def test_list_all_locks():

    # lock 1
    lock = lock_data[0]
    create_lock(lock)

    # lock 2
    lock = lock_data[1]
    create_lock(lock)

    r = request_session.get(f"{local_api}/v1/locks")
    assert r.status_code == 200


def test_list_all_locks_by_date():
    lock = lock_data[0]
    date = lock["event_date"]
    create_lock(lock)
    r = request_session.get(f"{local_api}/v1/locks/dates/{date}")
    assert r.status_code == 200


def test_delete_all_locks_by_date():
    lock = lock_data[0]
    date = lock["event_date"]
    create_lock(lock)
    r = request_session.delete(f"{local_api}/v1/locks/dates/{date}")
    assert r.status_code == 200
