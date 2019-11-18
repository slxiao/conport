from datetime import datetime, timedelta
import time

ONE_HOUR_IN_MS = 1 * 60 * 60 * 1000


def get_boundary_timestamps(past_hours):
    end_timestamp = int(time.time() * 1000)
    start_timestamp = end_timestamp - int(past_hours) * ONE_HOUR_IN_MS
    return (start_timestamp, end_timestamp)


def build_in_boundary(past_hours, timestamp):
    start_timestamp, end_timestamp = get_boundary_timestamps(past_hours)
    return True if timestamp >= start_timestamp and timestamp < end_timestamp else False
