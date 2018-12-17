
from datetime import datetime, timedelta
import re
import sys
from collections import namedtuple
from itertools import groupby
from operator import attrgetter, itemgetter

Log = namedtuple('Log', ['day', 'minute', 'guard', 'state'])

date_re = re.compile(r'\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\].*')
shift_start = re.compile(r'\[\d+-\d+-\d+ \d+:\d+\] #(\d+) begins shift')
guard_sleep = re.compile(r'\[\d+-\d+-\d+ \d+:\d+\] falls asleep')
guard_wakeup = re.compile(r'\[\d+-\d+-\d+ \d+:\d+\] wakes up')


def main(input_file):
    with open(input_file) as stream:
        lines = sorted(
            re.sub(
                'Guard ', '', re.sub('1518', '2018', stream.read())
            ).split('\n')
        )

    logs = sort_logs(lines)
    logs = parse_logs(logs)
    schedules = per_minute_schedule(logs)

    guard, minute = attack_vector_1(schedules)
    print 'Part 1:', guard * minute

    guard, minute = attack_vector_2(schedules)
    print 'Part 2:', guard * minute


def sort_logs(lines):
    return sorted(
        [
            (
                datetime(*[int(value) for value in date_re.match(line).groups()]),
                line
            )
            for line in lines
        ],
        key=itemgetter(0)
    )


def parse_logs(sorted_logs):
    logs = []
    for date, log in sorted_logs:
        if shift_start.match(log):
            current_guard = int(shift_start.match(log).group(1))
            if date.hour != 00:
                date += timedelta(days=1)
            logs.append(Log(date.strftime('%Y-%m-%d'), date.minute, current_guard, 'start'))
        elif guard_sleep.match(log):
            logs.append(Log(date.strftime('%Y-%m-%d'), date.minute, current_guard, 'sleep'))
        elif guard_wakeup.match(log):
            logs.append(Log(date.strftime('%Y-%m-%d'), date.minute, current_guard, 'wakeup'))

    return logs


def per_minute_schedule(logs):
    schedules = {}
    for guard_day, log_group in groupby(logs, key=attrgetter('guard', 'day')):
        log_group = list(log_group)
        for log_sleep, log_wakeup in zip(log_group[1::2], log_group[2::2]):
            if log_sleep.state != 'sleep':
                import pdb; pdb.set_trace()
            if log_wakeup.state != 'wakeup':
                import pdb; pdb.set_trace()
            sleep_start = log_sleep.minute
            sleep_end = log_wakeup.minute if log_wakeup else 61
            guard_schedule = schedules.setdefault(guard_day[0], {})
            for minute in range(sleep_start, sleep_end):
                guard_schedule[minute] = guard_schedule.get(minute, 0) + 1

    return schedules


def attack_vector_1(schedules):
    sleepiest_guard, guard_schedule = max(
        schedules.iteritems(),
        key=lambda guard_data: sum(guard_data[1].values())
    )
    sleepiest_minute, days_asleep = max(
        guard_schedule.iteritems(),
        key=itemgetter(1)
    )

    return sleepiest_guard, sleepiest_minute


def attack_vector_2(schedules):
    sleepiest_guard, sleepiest_minute, sleepiest_amount = None, None, 0
    for guard, schedule in schedules.iteritems():
        for minute, days_asleep in schedule.iteritems():
            if days_asleep > sleepiest_amount:
                sleepiest_guard, sleepiest_minute, sleepiest_amount = (
                    guard, minute, days_asleep
                )

    return sleepiest_guard, sleepiest_minute


if __name__ == '__main__':
    main(sys.argv[1])
