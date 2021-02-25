SOLVER=example

ifdef DEBUG
DEBUGSTR = --debug
else
DEBUGSTR =
endif

all: a b c d e f

zip:
	zip -r output/submission.zip . --exclude @.exclude.lst

a: zip
	python main.py input/a.txt --output output/a.txt --solver $(SOLVER) $(DEBUGSTR)

b: zip
	python main.py input/b.txt --output output/b.txt --solver $(SOLVER) $(DEBUGSTR)

c: zip
	python main.py input/c.txt --output output/c.txt --solver $(SOLVER) $(DEBUGSTR)

d: zip
	python main.py input/d.txt --output output/d.txt --solver $(SOLVER) $(DEBUGSTR)

e: zip
	python main.py input/e.txt --output output/e.txt --solver $(SOLVER) $(DEBUGSTR)

f: zip
	python main.py input/f.txt --output output/f.txt --solver $(SOLVER) $(DEBUGSTR)
