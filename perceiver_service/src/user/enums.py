from enum import Enum


class UserStatus(Enum):
    """
    Represent status of user account.

    Statuses:
        PAID: successfully paid
        UNPAID: unpaid
        DEACTIVATED: deactivated account
    """

    PAID = "paid"
    UNPAID = "unpaid"
    DEACTIVATED = "deactivated"
