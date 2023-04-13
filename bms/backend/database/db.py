import os
from pathlib import Path
from typing import Any, Literal, Optional, Union
from sqlmodel import SQLModel, Session, create_engine, select
from bms.backend.config import BMS_LOG_DIR
from bms.backend.logger import Logger


def create_sqlalchemy_loggers(stdout: bool = True):
    loggers = [
        "sqlalchemy.orm",
        "sqlalchemy.dialects",
        "sqlalchemy.pool",
        "sqlalchemy.engine",
    ]

    for _ in loggers:
        globals()[f"logger_{str(_).split('.')[-1]}"] = Logger(
            _,
            logging_file="bms_log",
            logging_dir=BMS_LOG_DIR,
            log_to_stdout=stdout,
        )


create_sqlalchemy_loggers()


logger_db: Logger = Logger(
    "bms.backend.database.db.DB",
    logging_file="bms_log",
    logging_dir=BMS_LOG_DIR,
    log_to_stdout=True,
)


class DB:
    def __init__(
        self,
        *,
        db_api: str,
        db_name: str,
        db_dir: Union[str, Path],
        echo: Union[bool, str],
        hide_parameters: bool,
    ) -> None:
        self.db_api = db_api
        self.db_name = db_name
        self.db_dir = db_dir

        # Engine:

        logger_db.info("Instantiated DB class")

        self.engine_url = f"{self.db_api}:///{str(self.db_dir.resolve())}{os.path.sep}{self.db_name}"
        self.engine = create_engine(
            self.engine_url, echo=echo, hide_parameters=hide_parameters
        )
        logger_db.debug(f"Created engine with URL: {self.engine_url}")
        logger_db.info("Creating all Tables")
        self.create_table_metadata()

    def create_table_metadata(self):
        try:
            SQLModel.metadata.create_all(self.engine)
        except Exception as e:
            logger_db.warning("Didn't create Tables")
            logger_db.exception(e)

    def insert_records(
        self, *, model_object: Union[list[SQLModel], SQLModel]
    ) -> bool:
        try:
            with Session(self.engine) as session:
                logger_db.info("Created Session - INSERT")
                if type(model_object) == list:
                    logger_db.info("Multiple Objects Given: `adding all`")
                    session.add_all(model_object)
                else:
                    logger_db.info("One Object Given: `add`")
                    session.add(model_object)

                logger_db.debug(f"Committed the object: {model_object}")
                session.commit()
                return True
        except Exception as e:
            logger_db.info("Unable to add Object to the database")
            logger_db.exception(e)
            return False
        finally:
            session.close()
            logger_db.info("Closed the Session - INSERT")

    def read_records(
        self,
        *,
        model_class: SQLModel,
        where_and_to: Optional[dict[str, Any]] = None,
        fetch_mode: Optional[Literal["all", "one", "many"]] = "all",
        how_many: Optional[int] = None,
    ) -> Any:
        """
        select(model).where(model.attribute == value)
        """

        with Session(self.engine) as session:
            logger_db.info("Created Session - READ")
            try:
                if where_and_to != None:
                    logger_db.info("Has a WHERE constraint")
                    logger_db.debug(f"WHERE: {where_and_to}")
                    statement = select(model_class).where(
                        getattr(model_class, list(where_and_to.keys())[0])
                        == list(where_and_to.values())[0]
                    )
                else:
                    logger_db.info("Has no WHERE constraint")
                    statement = select(model_class)
                    logger_db.debug(f"Created the `STATEMENT`: {statement}")

                logger_db.info("Executing SQL Query with the Session - READ")
                result = session.exec(statement)
                # print(result.all())
                logger_db.info("Fetching data from DataBase")
                logger_db.debug(f"Fetch Mode: {fetch_mode}")
                if fetch_mode == "all":
                    return result.all()
                elif fetch_mode == "one":
                    return result.one()  # handle error
                elif (
                    (fetch_mode == "many")
                    and (how_many != None)
                    and (how_many > 0)
                ):
                    return result.fetchmany(how_many)
                else:  # if no fetch_mode specified
                    logger_db.info(
                        "Executing the default `fetch_mode`:", fetch_mode
                    )
                    return result.all()
            except Exception as e:
                logger_db.warning("Unable to READ Data !!!")
                logger_db.exception(e)
            finally:
                session.close()
                logger_db.info("Closed Session - READ")

    def update_records(
        self, *, model_class: SQLModel, where_and_to: dict[str, Any]
    ):  # mistake : I need to update an SQLModel that has an attribute == value with attribute = new_value but i am setting the result without the crt object
        result = self.read_records(
            model_class=model_class,
            where_and_to=where_and_to,
            fetch_mode="one",
        )

        setattr(
            result,
            list(where_and_to.keys())[0],
            list(where_and_to.values())[0],
        )
        self.insert_records(model_object=result)
        with Session(self.engine) as session:
            try:
                logger_db.info("Created Session - UPDATE")
                logger_db.info("Refreshing the model to get the updated DATA")
                session.refresh(result)
                session.commit()

            except Exception as e:
                logger_db.warning()
                logger_db.debug(f"Exception:\n {e}\nLocals:\n{locals()}")
            finally:
                logger_db.info("Closing Session - UPDATE")
                session.close()

    def delete_records(
        self, *, model_class: SQLModel, where_and_to: dict[str, Any]
    ) -> bool:
        try:
            with Session(self.engine) as session:
                logger_db.info("Created Session - DELETE")

                statement = select(model_class).where(
                    getattr(model_class, list(where_and_to.keys())[0])
                    == list(where_and_to.values())[0]
                )
                logger_db.info("Created the delete statement")
                logger_db.debug(f"DELETE statement: {statement}")
                result = session.exec(statement).one()  # need to work on this
                logger_db.info("Deleting Object")
                logger_db.debug(f"Deleting the object: {result}")

                session.delete(result)
                session.commit()
                return True
        except Exception as e:
            logger_db.warning(f"Error deleting records")
            logger_db.exception(f"Exception:\n{e}\nLocals:\n{locals()}")
            return False
        finally:
            logger_db.info("Closing Session - DELETE")
            session.close()
