from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

"""
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    icloud_account_id: Optional[int] = Field(default=None, foreign_key="icloudaccount.id")
    icloud_account: Optional["ICloudAccount"] = Relationship(back_populates="user")


class ICloudAccount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="icloud_account"
    )
"""


# class FixedDeposit(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     applicant: str = Field(nullable=False)
#     bank: str = Field(nullable=False)
#     principal_amount: float = Field(nullable=False)
#     interest: float = Field(nullable=False)
#     interest_period_in_months: int = Field(nullable=False)
#     maturity_amount: float = Field(nullable=False)
#     interest_amount: float = Field(nullable=False)


class RecurringDeposit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    applicant: str = Field(nullable=False)
    bank: str = Field(nullable=False)
    principal_amount: float = Field(nullable=False)
    interest: float = Field(nullable=False)
    compounding_periods: int = Field(nullable=False)
    interest_period_in_months: int = Field(nullable=False)
    maturity_amount: float = Field(nullable=False)
    interest_amount: float = Field(nullable=False)
