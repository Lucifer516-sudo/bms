from bms.backend.computer import Compute
from bms.backend.database.db import DB
from bms.backend.database.models import RecurringDeposit
from bms.backend.config import BMS_DB_DIR


bms_db: DB = DB(
    db_api="sqlite",
    db_name="BMS_DB.db",
    db_dir=BMS_DB_DIR,
    echo=False,
    hide_parameters=False,
)
bms_db.create_table_metadata()


compute = Compute()


def simple_interest(P: float, n: float, r: float):
    return compute.simple_interest(P, n, r)


def compound_interest(P: float, n: int, r: float, t: int):
    return compute.compound_interest(P, n, r, t)
