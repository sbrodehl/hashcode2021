from dataclasses import dataclass, field, InitVar

from .pizza import Pizza


@dataclass
class Delivery:
    """Class representing a pizza delivery."""
    team_size: int
    pizza_ids: set[int] = field(default_factory=set)
    ingredients: set[int] = field(default_factory=set, init=False, repr=False)
    pizzas: InitVar[list[Pizza]] = None

    def add(self, pizza: Pizza):
        if pizza.id not in self.pizza_ids:
            self.pizza_ids.add(pizza.id)
            pizza.delivered = True
            self.ingredients.update(pizza.ingredients)

    def __post_init__(self, pizzas: list[Pizza]):
        if len(self.pizza_ids) > 0 and pizzas is not None:
            self.ingredients = set().union(*[p.ingredients for p in pizzas if p.id in self.pizza_ids])

    def __len__(self):
        return len(self.pizza_ids)

    def complete(self):
        return self.team_size == len(self)

    def empty(self):
        return 0 == len(self)
