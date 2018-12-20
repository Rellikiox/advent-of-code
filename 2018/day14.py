from __future__ import print_function
import sys


def main(target_recipes, print_enabled):
    print('Part 1:', part_1(target_recipes, print_enabled))
    print('Part 2:', part_2(target_recipes, print_enabled))


def part_1(target_recipes, print_enabled):
    target_recipes = int(target_recipes)
    return ''.join(
        [str(val) for val in RecipeList()[target_recipes:target_recipes + 10]]
    )


def part_2(target_recipe, print_enabled):
    target_recipe = bytearray(int(val) for val in target_recipe)
    recipes = RecipeList()

    recipe_index = 0
    while True:
        for target_index, character in enumerate(target_recipe):
            if character != recipes[recipe_index + target_index]:
                break
        else:
            return recipe_index
        recipe_index += 1


class RecipeList(object):
    def __init__(self):
        self.elf_1, self.elf_2 = 0, 1
        self.recipes = bytearray([3, 7])

    def __getitem__(self, index):
        if isinstance(index, slice):
            target_length = index.stop
        else:
            target_length = index

        while target_length >= len(self.recipes):
            self.recipes.extend(
                [int(val) for val in str(self.recipes[self.elf_1] + self.recipes[self.elf_2])]
            )
            self.elf_1 = (self.elf_1 + (self.recipes[self.elf_1] + 1)) % len(self.recipes)
            self.elf_2 = (self.elf_2 + (self.recipes[self.elf_2] + 1)) % len(self.recipes)

        return self.recipes[index]

    def __len__(self):
        return len(self.recipes)


if __name__ == '__main__':
    print_enabled = 'print_enabled' in sys.argv
    main(sys.argv[1], print_enabled)
