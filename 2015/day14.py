
from operator import attrgetter
import sys
import re

line_re = re.compile(
    r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.'
)


class Flier(object):
    def __init__(self, name, speed, rest_interval, rest_duration):
        self.name = name
        self.speed = speed
        self.rest_interval = rest_interval
        self._rest_interval = rest_interval
        self.rest_duration = rest_duration
        self._rest_duration = rest_duration
        self.is_flying = True
        self.distance_flown = 0
        self.points = 0


def main(input_file, target_time):
    fliers = []
    with open(input_file) as stream:
        for line in stream:
            name, speed, rest_interval, rest_duration = line_re.match(line).groups()
            fliers.append(Flier(
                name, int(speed), int(rest_interval), int(rest_duration)
            ))

    for i in range(int(target_time)):

        for flier in fliers:
            if flier.is_flying:
                flier.rest_interval -= 1
                flier.distance_flown += flier.speed
                if flier.rest_interval == 0:
                    flier.rest_interval = flier._rest_interval
                    flier.is_flying = False
            else:
                flier.rest_duration -= 1
                if flier.rest_duration == 0:
                    flier.rest_duration = flier._rest_duration
                    flier.is_flying = True

        lead_distance = max(fliers, key=attrgetter('distance_flown')).distance_flown
        for flier in fliers:
            if flier.distance_flown == lead_distance:
                flier.points += 1


    print 'Part 1:', max(fliers, key=attrgetter('distance_flown')).distance_flown
    print 'Part 2:', max(fliers, key=attrgetter('points')).points


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
