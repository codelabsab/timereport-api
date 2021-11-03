import os
from chalice import Chalice
from chalicelib.v1_routes import v1_routes
from chalicelib.model.models import EventTable, LockTable
import logging


for db_instance in [EventTable, LockTable]:
    if not db_instance.exists():
        db_instance.create_table(
            read_capacity_units=1, write_capacity_units=1, wait=True
        )


app = Chalice(app_name="timereport_backend")
app.register_blueprint(v1_routes)

app.debug = os.getenv("BACKEND_DEBUG", False)
log_level = logging.DEBUG if app.debug else logging.INFO
app.log.setLevel(log_level)
