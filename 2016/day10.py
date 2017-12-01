
import re


action_re = r'bot (\d+) gives (high|low) to (bot|output) (\d+) and (high|low) to (bot|output) (\d+)'

test_input = """value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


class Bot(object):
    def __init__(self, bot_id):
        self.id = bot_id
        self.values = []
        self.queue = []

    def pop(self, action):
        return getattr(self, 'pop_' + action)()

    def pop_high(self):
        return self.values.pop(-1)

    def pop_low(self):
        return self.values.pop(0)

    def give(self, action, bot):
        getattr(self, 'give_' + action)(bot)

    def give_high(self, bot):
        bot.take(self.pop_high())

    def give_low(self, bot):
        bot.take(self.pop_low())

    def take(self, value):
        self.values = sorted(self.values + [value])
        if len(self.values) == 2 and self.values[0] == 17 and self.values[1] == 61:
            print '-------------', self.id

    def can_act(self):
        return len(self.values) == 2

    def __repr__(self):
        return '{}: {}'.format(self.id, self.values)


def run_bots(input):
    input = input.strip()

    bots = {}
    for init_match in re.findall(r'value (\d+) goes to bot (\d+)', input):
        value = int(init_match[0])
        bot_id = int(init_match[1])
        bots.setdefault(bot_id, Bot(bot_id)).take(value)

    outputs = {}
    actions = re.findall(action_re, input)
    while actions:
        action = actions.pop(0)
        bot_id = int(action[0])
        bot = bots.get(bot_id)
        if bot is None or not bot.can_act():
            actions.append(action)
            continue

        do_action(bot_id, action[1:4], bots, outputs)
        do_action(bot_id, action[4:7], bots, outputs)

    return bots, outputs


def do_action(bot_id, action, bots, outputs):
    value, dest = action[0:2]
    dest_id = int(action[2])
    if dest == 'bot':
        bots[bot_id].give(value, bots.setdefault(dest_id, Bot(dest_id)))
    else:
        outputs.setdefault(dest_id, []).append(bots[bot_id].pop(value))


def main():
    run_bots(test_input)


if __name__ == '__main__':
    main()
