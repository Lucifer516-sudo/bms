from pathlib import Path

BMS_HOME: Path = Path().home() / "PyBMS"
BMS_LOG_DIR: Path = BMS_HOME / "BMS_Logs"
BMS_DB_DIR: Path = BMS_HOME / "BMS_DB"


def bms_mkdir():
    if not BMS_HOME.exists():
        BMS_HOME.mkdir()
    if not BMS_LOG_DIR.exists():
        BMS_LOG_DIR.mkdir()
    if not BMS_DB_DIR.exists():
        BMS_DB_DIR.mkdir()


bms_mkdir()
