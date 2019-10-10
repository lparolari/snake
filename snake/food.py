import random

from snake.board import Entity


class Food(Entity):

    _flowers = []

    def one(self, available):
        self._flowers.append(available[random.randrange(0, len(available))])

    def more(self, n, available):
        for i in range(n):
            self.one(available)

    def eat(self, food):
        self._flowers.remove(food)

    def to_list(self):
        return self._flowers.copy()
