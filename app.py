import os
from chalice import Chalice
from chalicelib.lib import dynamo
from chalicelib.model import Dynamo
import logging
"""
GET        /table-name  : returns name of dynamodb table (good for testing connection)
GET        /user/<user_id>
GET        /user/<user_id>?startDate=YYYYMMDD&endDate=YYYYMMDD
POST       /event
#######################
# We don't insert any _id at this time
# Do we really need GET/PUT/DELETE for event?
# is not user_id + event_date sufficient to PUT/DELETE an event?
GET        /event/<_id>
GET        /event/?startDate=YYYYMMDD&endDate=YYYYMMDD
PUT        /event/<_id>
DELETE     /event/<_id>


{'user_id': 'U2FGC795G', 'user_name': 'kamger', 'reason': 'vab', 'event_date': datetime.datetime(2018, 12, 5, 0, 0), 'hours': '8'}
{"user_id": "U2FGC795G", "user_name": "kamger", "reason": "vab", "event_date": "2018-12-03", "hours":8}
"""

app = Chalice(app_name='timereport_backend')
app.debug = os.getenv('BACKEND_DEBUG', False)
log = logging.getLogger(__name__)

db = Dynamo.EventModel
# create the table
if not db.exists():
    log.info('database table do not exist, creating it')
    db.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

@app.route('/table-name', cors=True)
def test_name():
    """
    :return: table name
    """
    return {'name': dynamo.dynamoboto.table.name }

@app.route('/user/names', methods=['GET'], cors=True)
def get_user_names():
    return dynamo.get_user_names()

@app.route('/user/{user_id}', methods=['GET'], cors=True)
def get_user_by_id(user_id):

    if app.current_request.query_params:
        start_date = app.current_request.query_params.get('startDate')
        end_date = app.current_request.query_params.get('endDate')
        return dynamo.get_user_between_date(user_id, start_date, end_date)
    else:
        return dynamo.get_id(user_id)

@app.route('/event', methods=['POST'], cors=True)
def create_event():
    dynamo.create_event(app.current_request.json_body)
    return app.current_request.json_body

@app.route('/event/{_id}', methods=['GET'], cors=True)
def get_event_by_id(_id):
    return {'event_id': _id}

@app.route('/event/{_id}', methods=['PUT'], cors=True)
def put_event_by_id(_id):
    return app.current_request.json_body

@app.route('/event/{_id}', methods=['DELETE'], cors=True)
def delete_event_by_id(_id):
    if app.current_request.query_params:
        start_date = app.current_request.query_params.get('date')
        app.log.info(f'delete event backend: date is {start_date} and id is {_id}')
        return dynamo.delete_event(_id, start_date)