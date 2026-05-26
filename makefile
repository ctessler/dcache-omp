.PHONY: graphs clean notused

BIN := dcache-omp
OUT := out
GRP := graph
USE := unused

all: graphs notused

graphs: $(OUT)/calc.csv | $(GRP)
	$(BIN)/g-agg.py $(OUT)/calc.csv --pfx=$(GRP)/g-agg. --ext=.eps
	$(BIN)/g-bars.py $(OUT)/calc.csv --pfx=$(GRP)/g-bar --ext=.eps

notused: $(OUT)/calc.csv | $(USE)
	# Keep these building...
	$(BIN)/gratios.py $(OUT)/calc.csv $(USE)/g-ratio.
	$(BIN)/gimp.py $(OUT)/calc.csv $(USE)/g-imp.

$(OUT)/calc.csv : $(OUT)/compiled.csv
	$(BIN)/add-cols.py $(OUT)/compiled.csv $(OUT)/calc.csv

$(OUT)/compiled.csv : $(OUT)/list.txt
	$(BIN)/compile-csvs.py $(OUT)/list.txt $(OUT)/compiled.csv

$(OUT)/list.txt: | $(OUT)
	$(BIN)/find-csvs.sh > $(OUT)/list.txt

$(OUT) $(GRP) $(USE):
	mkdir $@

clean:
	rm -rf $(OUT) $(GRP) $(USE)
