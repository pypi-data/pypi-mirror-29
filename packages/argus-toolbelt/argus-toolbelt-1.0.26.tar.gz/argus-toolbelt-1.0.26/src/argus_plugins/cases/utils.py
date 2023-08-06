"""This is a helper module for all things case related"""
import time
from datetime import datetime

from argus_api.api.customers.v1.customer import get_customer_by_shortname
from argus_cli.settings import settings

STATUSES = ["pendingCustomer", "pendingSoc", "pendingVendor", "workingSoc", "workingCustomer", "pendingClose", "closed"]
SERVICE_TYPES = ["securityIncident", "operationalIncident", "informational", "change"]
PRIORITIES = ["low", "medium", "high", "critical"]


def get_customer_id(name: str) -> int:
    """Gets a customer's ID from their name

    :param name: The name of the customer
    """
    customers = get_customer_by_shortname(apiKey=settings["api"]["api_key"], shortName=name.lower())["data"]
    customer_id = customers["id"]  # This might get the wrong customer if there are more with the same name?
    return customer_id


def date_time_to_timestamp(input):
    """Parses a time argument in a ISO8601 format

    Can either be just date, or date + time
    """
    if len(input) is len("YYYY-mm-dd"):
        time_format = "%Y-%m-%d"
    elif len(input) is len("YYYY-mm-ddTHH-MM-SS"):
        time_format = "%Y-%m-%dT%H:%M:%S"
    elif input == "now":
        return int(time.mktime(datetime.now().timetuple()) * 1e3)  # Add milliseconds
    else:
        raise ValueError("Invalid time input-format. Use ISO8601 format")
    date = datetime.strptime(input, time_format)
    return int(time.mktime(date.timetuple()) * 1e3)


def time_diff(input):
    """Converts the input from one unit to milliseconds"""
    units = {"s": 1, "m": 60, "h": 60 * 60, "d": 60 * 60 * 24, "w": 60 * 60 * 24 * 7}
    if input == "now":
        return 0
    else:
        return int(input[:-1]) * units[input[-1]] * 1000


def timestamp_to_period(timestamp: int):
    """Converts a timestamp to a ISO8601 style period with days"""
    return datetime.fromtimestamp(timestamp).strftime("P%jDT%H:%M:%S")


def timestamp_to_date(timestamp: int):
    """Converts a timestamp to a ISO8601 style date and time"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S")

