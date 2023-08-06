"""
Convert time_limit_string string [ex. 22h5m] to total minute count [ex. 1325]
"""

import re as regexp

MINUTES_IN_HOUR = 60
TIME_LIMIT_REGEXP = "\\b(\\d+)h\\b|\\b(\\d+)m\\b|\\b(\\d+)h(\\d+)m\\b"

def main(time_limit_string):

    match = regexp.match(TIME_LIMIT_REGEXP, time_limit_string, flags=regexp.IGNORECASE)

    if not match:
        raise ValueError("Invalid time_limit_string, regexp did not match")

    all_groups = match.groups()
    groups = all_groups[:2] if all_groups[1] or all_groups[0] else all_groups[2:4]
    groups = tuple(map(lambda group: int(group or 0), groups))
    hours, minutes = groups

    return hours * MINUTES_IN_HOUR + minutes
