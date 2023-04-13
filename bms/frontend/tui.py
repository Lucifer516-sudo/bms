from typing import Any
from rich.console import Console
from rich.table import Table
from bms.backend.bms_functions import compound_interest, bms_db
from bms.backend.database.models import RecurringDeposit
from bms.backend.logger import Logger


class TUI_Widgets:
    def __init__(self, console: Console) -> None:
        self.log = Logger("bms.frontend.tui.TUI_Widgets")
        self.console = console

    def table(
        self,
        name: str,
        column: list[str],
        rows: list[list[str]],
    ):
        try:
            if self.console.is_alt_screen():
                self.log.debug(
                    f"Secondary Screen: {self.console.is_alt_screen()}"
                )
                table_ = Table(title=name, show_lines=True)
                self.log.info("Create an Rich Table")
                self.log.debug(f"Rich Table Name: `{table_}`")

                for attribute in column:
                    table_.add_column(
                        str(attribute), justify="center", overflow="fold"
                    )

                self.log.debug(
                    f"Rich Table:\n{' '*25}Column: {column}\n{' '*25}Rows: {rows}"
                )

                for record in rows:
                    if len(record) == len(column):
                        table_.add_row(*tuple(record))
                self.log.info("Created the Rich Table")
                self.log.debug(f"Rich Table: {table_.__repr__()}")

                return table_
        except Exception as e:
            self.log.info("Encountered Error while creating Table")
            self.log.debug(f"Locals: {locals()}\nGlobals: {globals()}")
            self.log.exception(e)

    def create_secondary_screen(self):
        try:
            self.log.debug(
                f"Secondary Screen Enabled: {self.console.is_alt_screen()}"
            )
            if not self.console.is_alt_screen():
                self.log.info("Trying to create a Secondary Screen")
                self.console.screen()
                self.log.debug(
                    f"Enabled Secondary Screen: {self.console.is_alt_screen()}"
                )
        except Exception as e:
            self.log.info("Encountered Error while creating Secondary Screen")
            self.log.debug(f"Locals: {locals()}\nGlobals: {globals()}")
            self.log.exception(e)


class TUI_DB_Functions:
    def __init__(self) -> None:
        self.db = bms_db
        self.RD = RecurringDeposit

    def add_rd(
        self,
        applicant: str,
        bank: str,
        P: float,
        r: float,
        n: int = 4,
        t: int = 12,
    ):
        ci, amount = compound_interest(P, n, r, t)
        rd_object = self.RD(
            applicant=applicant,
            bank=bank,
            principal_amount=P,
            interest=r,
            compounding_periods=n,
            interest_period_in_months=t,
            maturity_amount=ci,
            interest_amount=amount,
        )
        self.db.insert_records(model_object=rd_object)
        return rd_object

    def update_rd(self):
        self.db.update_records()
