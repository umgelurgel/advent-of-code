import re
from collections import defaultdict
from dateutil import parser


if __name__ == '__main__':
    with open("input.txt", "r") as file:
        # Remove empty lines
        lines = [line for line in file.read().split('\n') if line]

    # [1518-10-22 00:26] falls asleep
    # [1518-07-24 23:47] Guard #3319 begins shift
    regex_str = r'^\[(?P<timestamp>.+)\] (?P<detail>.+)'
    regex = re.compile(regex_str)

    log = []
    for line in lines:
        parsed = regex.match(line).groupdict()
        timestamp = parser.parse(parsed['timestamp'])
        detail = parsed['detail']

        log.append({
            'timestamp': timestamp,
            'detail': detail,
        })

    log.sort(key=lambda x: x['timestamp'])

    start_watch_regex_str = r'^Guard #(?P<guard_id>\d+) begins shift'
    start_watch_regex = re.compile(start_watch_regex_str)

    last_guard_id = None
    last_asleep_start = None
    guard_asleep_minutes = defaultdict(lambda: defaultdict(int))

    for entry in log:
        detail = entry['detail']
        start_watch_result = start_watch_regex.match(detail)
        if start_watch_result:
            last_guard_id = int(start_watch_result.groupdict()['guard_id'])
        elif detail == 'falls asleep':
            last_asleep_start = entry['timestamp']
        elif detail == 'wakes up':
            asleep_minutes = int((entry['timestamp'] - last_asleep_start).seconds / 60)

            start_minute = last_asleep_start.minute
            for minute_delta in range(asleep_minutes):
                guard_asleep_minutes[last_guard_id][start_minute + minute_delta] += 1

    max_same_minute_count = 0
    max_same_minute_guard_id = None
    for guard_id, minutes_asleep in guard_asleep_minutes.items():
        max_same_minute_current = max(minutes_asleep.values())
        if max_same_minute_current > max_same_minute_count:
            max_same_minute_count = max_same_minute_current
            max_same_minute_guard_id = guard_id

    most_common_minute = [
        minute for minute, count in guard_asleep_minutes[max_same_minute_guard_id].items() if count == max_same_minute_count
    ][0]

    print(f'The product is: {most_common_minute * max_same_minute_guard_id}')