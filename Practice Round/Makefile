SOLVER=example

ifdef DEBUG
DEBUGSTR = --debug
else
DEBUGSTR =
endif

all: example littlebitofeverything manyingredients manypizzas manyteams

zip:
	zip -r output/submission.zip . --exclude @.exclude.lst

example: zip
	python main.py input/a_example.in --output output/a_example.out --solver $(SOLVER) $(DEBUGSTR)

littlebitofeverything: zip
	python main.py input/b_little_bit_of_everything.in --output output/b_little_bit_of_everything.out --solver $(SOLVER) $(DEBUGSTR)

manyingredients: zip
	python main.py input/c_many_ingredients.in --output output/c_many_ingredients.out --solver $(SOLVER) $(DEBUGSTR)

manypizzas: zip
	python main.py input/d_many_pizzas.in --output output/d_many_pizzas.out --solver $(SOLVER) $(DEBUGSTR)

manyteams: zip
	python main.py input/e_many_teams.in --output output/e_many_teams.out --solver $(SOLVER) $(DEBUGSTR)
