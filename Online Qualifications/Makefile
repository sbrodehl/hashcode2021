SOLVER=heuristics

ifdef DEBUG
DEBUGSTR = --debug
else
DEBUGSTR =
endif

all: a b c d e f g

json:
	find input -type f -iname "*.txt" -exec python main.py --json $(DEBUGSTR) {} \;

zip:
	rm -f output/submission.zip && zip -r output/submission.zip . --exclude @.exclude.lst

a: zip
	python main.py input/a_an_example.txt --output output/a_an_example.txt --solver $(SOLVER) $(DEBUGSTR)

b: zip
	python main.py input/b_by_the_ocean.txt --output output/b_by_the_ocean.txt --solver $(SOLVER) $(DEBUGSTR)

c: zip
	python main.py input/c_checkmate.txt --output output/c_checkmate.txt --solver $(SOLVER) $(DEBUGSTR)

d: zip
	python main.py input/d_daily_commute.txt --output output/d_daily_commute.txt --solver $(SOLVER) $(DEBUGSTR)

e: zip
	python main.py input/e_etoile.txt --output output/e_etoile.txt --solver $(SOLVER) $(DEBUGSTR)

f: zip
	python main.py input/f_forever_jammed.txt --output output/f_forever_jammed.txt --solver $(SOLVER) $(DEBUGSTR)

g: zip
	python main.py input/g_kaggle.txt --output output/g_kaggle.txt --solver $(SOLVER) $(DEBUGSTR)
