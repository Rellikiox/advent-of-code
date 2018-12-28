
from operator import attrgetter
import sys
import re

units_re = re.compile(
    r'(\d+) units each with (\d+) hit points ?(\([^\)]*\))? with an '
    r'attack that does (\d+) (\w+) damage at initiative (\d+)'
)


def parse_traits(raw_traits):
    if not raw_traits:
        return [], []

    traits = {}
    trait_texts = raw_traits[1:-1].split('; ')
    for trait_string in trait_texts:
        trait_type, trait_values = trait_string.split(' to ')
        traits[trait_type] = trait_values.split(', ')
    return traits.get('weak', []), traits.get('immune', []),


def parse_input(input_data):
    raw_immune_text, raw_infection_text = input_data.split('\n\n')
    immune_units = [
        UnitGroup.from_input(line, 'immune', idx)
        for idx, line in enumerate(raw_immune_text.strip().split('\n')[1:])
    ]
    infection_units = [
        UnitGroup.from_input(line, 'infection', idx)
        for idx, line in enumerate(raw_infection_text.strip().split('\n')[1:])
    ]
    return immune_units, infection_units


class UnitGroup(object):
    @classmethod
    def from_input(cls, input_row, unit_type, unit_idx):
        unit_size, hitpoints, raw_traits, damage, damage_type, initiative = (
            units_re.match(input_row).groups()
        )
        weaknesses, immunities = parse_traits(raw_traits)
        return cls(
            unit_type=unit_type,
            unit_idx=unit_idx,
            unit_size=int(unit_size),
            hitpoints=int(hitpoints),
            damage=int(damage),
            damage_type=damage_type,
            initiative=int(initiative),
            weaknesses=weaknesses,
            immunities=immunities,
        )

    def __init__(
        self, unit_type, unit_idx, unit_size, hitpoints, damage,
        damage_type, initiative, weaknesses, immunities
    ):
        self.unit_type = unit_type
        self.idx = unit_idx
        self.unit_size = unit_size
        self.hitpoints = hitpoints
        self.damage = damage
        self.damage_type = damage_type
        self.initiative = initiative
        self.weaknesses = weaknesses
        self.immunities = immunities

    @property
    def effective_power(self):
        return self.unit_size * self.damage

    def target_unit(self, enemy_units):
        best_targets = []
        for enemy in enemy_units:
            potential_damage = self.damage_to(enemy)
            if potential_damage == 0:
                continue

            if not best_targets or potential_damage > self.damage_to(best_targets[0]):
                best_targets = [enemy]
            elif potential_damage == self.damage_to(best_targets[0]):
                best_targets.append(enemy)
        if best_targets:
            target_unit = sorted(best_targets, key=self.enemy_selection_sort_order)[0]
            return target_unit, self.damage_to(target_unit)
        else:
            return None, None

    def damage_to(self, enemy):
        if self.damage_type in enemy.immunities:
            return 0

        return self.effective_power * (2 if self.damage_type in enemy.weaknesses else 1)

    def take_damage(self, damage):
        killed_units = min(damage / self.hitpoints, self.unit_size)
        self.unit_size -= killed_units
        return killed_units

    @property
    def is_dead(self):
        return self.unit_size <= 0

    @property
    def enemy_unit_type(self):
        return 'immune' if self.unit_type == 'infection' else 'infection'

    def targeting_sort_order(self):
        return (-self.effective_power, -self.initiative)

    def enemy_selection_sort_order(self, enemy):
        return (-enemy.effective_power, -enemy.initiative)


class CombatSystem(object):
    def __init__(self, immunity_units, infection_units, no_output):
        self.units = {
            'immune': immunity_units,
            'infection': infection_units
        }
        self.no_output = no_output

    def war(self):
        battle_continues = True
        while all(units for units in self.units.values()) and battle_continues:
            battle_continues = self.battle()

    def battle(self):
        self.print_current_state()

        # Targeting
        targeting_order = sorted(
            self.units['immune'] + self.units['infection'],
            key=UnitGroup.targeting_sort_order
        )
        attacking_units = []
        targets = []
        for unit in targeting_order:
            potential_targets = [
                enemy
                for enemy in self.units[unit.enemy_unit_type]
                if enemy not in targets
            ]
            defender, damage = unit.target_unit(potential_targets)
            if defender:
                attacking_units.append((unit, defender, damage))
                targets.append(defender)

        self.print_targets(attacking_units)

        # Attacking
        attacking_order = sorted(
            attacking_units,
            key=lambda attacking_data: -attacking_data[0].initiative
        )
        attacks = []
        total_units_killed = 0
        for attacker, defender, _ in attacking_order:
            if attacker.is_dead or defender.is_dead:
                continue
            units_killed = defender.take_damage(attacker.damage_to(defender))
            attacks.append((attacker, defender, units_killed))
            total_units_killed += units_killed

        if total_units_killed == 0:
            return False

        self.units['immune'] = [u for u in self.units['immune'] if not u.is_dead]
        self.units['infection'] = [u for u in self.units['infection'] if not u.is_dead]

        self.print_attacks(attacks)
        return True

    def size_of_remaining_unit(self):
        return max(
            sum(unit.unit_size for unit in units)
            for units in self.units.values()
        )

    def immune_won(self):
        return not self.units['infection']

    def size_of_immune(self):
        return sum(
            unit.unit_size
            for unit in self.units['immune']
        )

    def boost_immune_units(self, boost):
        for unit in self.units['immune']:
            unit.damage += boost

    def print_current_state(self):
        if self.no_output:
            return

        print 'Immune System:\n{}'.format(
            '\n'.join([
                'Group {} contains {} units'.format(unit.idx + 1, unit.unit_size)
                for unit in self.units['immune']
            ])
        )
        print 'Infection:\n{}'.format(
            '\n'.join([
                'Group {} contains {} units'.format(unit.idx + 1, unit.unit_size)
                for unit in self.units['infection']
            ])
        )
        print

    def print_targets(self, targets):
        if self.no_output:
            return

        for atacking, receiving, damage in targets:
            print '{} group {} would deal defending group {} {} damage'.format(
                atacking.unit_type.capitalize(), atacking.idx + 1, receiving.idx + 1, damage
            )
        print

    def print_attacks(self, attacks):
        if self.no_output:
            return

        for atacking, receiving, dead_units in attacks:
            print '{} group {} attacks defending group {}, killing {} units'.format(
                atacking.unit_type.capitalize(), atacking.idx + 1, receiving.idx + 1, dead_units
            )
        print


def main(input_filename, no_output):
    with open(input_filename) as stream:
        data = stream.read().strip()

    immune, infection = parse_input(data)

    combat = CombatSystem(list(immune), list(infection), no_output)
    combat.war()
    print 'Part 1:', combat.size_of_remaining_unit()

    boost = lower_bound = 2
    upper_bound = None
    while upper_bound is None:
        print 'Trying to boost by {}'.format(boost)
        immune, infection = parse_input(data)
        combat = CombatSystem(list(immune), list(infection), no_output)
        combat.boost_immune_units(boost)
        combat.war()
        immune_size = combat.size_of_immune()
        print 'Immune after battle: {}'.format(immune_size)
        if combat.immune_won():
            upper_bound = boost
        else:
            lower_bound = boost
            boost *= 2
    print 'Min boost is between {} and {}'.format(lower_bound, upper_bound)

    min_boost = None
    while min_boost is None:
        boost = (lower_bound + upper_bound) / 2
        immune, infection = parse_input(data)
        combat = CombatSystem(list(immune), list(infection), no_output)
        combat.boost_immune_units(boost)
        combat.war()
        immune_size = combat.size_of_immune()
        if combat.immune_won():
            print '{} <{}] {}'.format(lower_bound, boost, upper_bound)
            upper_bound = boost

            if (upper_bound - lower_bound) <= 2:
                min_boost = boost
        else:
            print '{} [{}> {}'.format(lower_bound, boost, upper_bound)
            if lower_bound == boost:
                upper_bound += 1
            else:
                lower_bound = boost

    print 'Part 2:', immune_size


if __name__ == '__main__':
    main(sys.argv[1], 'no_output' in sys.argv)
