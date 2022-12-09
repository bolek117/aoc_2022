from typing import List


class Elf:
    def __init__(self):
        self.sum: int = 0
        self.elements: List[int] = []

    def add_calories(self, calories: int) -> None:
        self.elements.append(calories)
        self.sum += calories

    def __str__(self):
        return f'{self.sum}: {", ".join(str(e) for e in self.elements)}'

    def __repr__(self):
        return self.__str__()


def get_elfs():
    with open('input.txt', 'r') as f:
        file_data = f.readlines()

    elfs = []
    elf = Elf()
    for line in file_data:
        line = line.strip()

        if len(line) == 0:
            elfs.append(elf)
            elf = Elf()
            continue

        calories = int(line)
        elf.add_calories(calories)

    elfs.append(elf)
    print('\n'.join([str(e) for e in elfs]))

    return elfs


def main():
    elfs = get_elfs()
    max_calories = max([e.sum for e in elfs])

    print('\n--- Part 1 ---')
    print(max_calories)


if __name__ == '__main__':
    main()
