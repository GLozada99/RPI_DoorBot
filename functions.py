import time


def has_time_passed(time_since, interval):
    # returns true if interval of time has passed since a specific time
    return True if (time.time() - time_since) > interval else False
