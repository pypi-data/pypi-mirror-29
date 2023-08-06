TOP:=$(shell pwd)/..

PYVER:=$(strip $(PYVER))

ifeq (,$(findstring $(PYVER),2 3))
$(error error variable PYVER must be set to 2 or 3)
endif

export PYVER

# set PYTHON only if it is not yet defined:
ifeq (,$(PYTHON))
        PYTHON:=python$(PYVER)
endif

BINDIR:=$(TOP)/python$(PYVER)/bin
LIBDIR:=$(TOP)/python$(PYVER)/pyexpander

export PYTHONPATH:=$(TOP)/python$(PYVER):$(PYTHONPATH)

ifeq ($(PYVER),2)
EXPANDER_BIN=expander.py
else
EXPANDER_BIN=expander3.py
endif

EXPANDER=$(BINDIR)/$(EXPANDER_BIN)

# The list of tests and their order is taken from file "TESTS":
expander_tests:= $(shell cat TESTS | xargs)


.PRECIOUS: %.out

# set this only to "yes" in order to create the 
# test[n].ok files. These files are later compared to
# the test[n].out files.
# In order for the tests to really test pyexpander, 
# the variable MUST BE set to "no".
CREATE_TESTS=no

all: pure_module_test external_module_test $(addsuffix .tst, $(expander_tests))

clean:
	rm -f $(addsuffix .out, $(expander_tests))

_clean: clean
	rm -f $(addsuffix .ok, $(expander_tests))

pure_module_test:
	echo "PYTHONPATH: " $(PYTHONPATH)
	$(PYTHON) $(LIBDIR)/parser.py
	$(PYTHON) $(LIBDIR)/lib.py

external_module_test:
	$(PYTHON) ./pyexpander_test.py

ok: $(addsuffix .ok, $(expander_tests))

%.out: %.in
	$(EXPANDER) -f $< > $@

external-variable.out: external-variable.in
	$(EXPANDER) -f $< --eval 'x=1' > $@

variable-undefined.out: variable-undefined.in
	($(EXPANDER) -f $< || true) 2>&1 | \
	    sed -e 's/.*\//  "/;s/line [0-9]\+/line xxx/;s/$(EXPANDER_BIN)/expander.py/;s/\(raise\) NameError, \(.*\)/\1 e.__class__(\2)/;s/\(str(e),\)\([^ ]\)/\1 \2/' > $@

simple-vars-option.out: simple-vars-option.in
	$(EXPANDER) -s -f $< > $@

include-path.out: include-path.in
	mkdir x
	echo "\$$py(a+=1)" > x/test.inc
	$(EXPANDER) -f $< -I x > $@
	rm -rf x

for-functionlist.out: for-functionlist.in
	$(EXPANDER) -f $< | sed -e 's/<type/<class/' > $@

stdin.out: stdin.in
	$(EXPANDER) < $< > $@

keyword-conflict.out: keyword-conflict.in
	($(EXPANDER) -f $< || true) 2>&1 | \
	    sed -e 's/.*\//  "/;s/line [0-9]\+/line xxx/;s/$(EXPANDER_BIN)/expander.py/;' > $@

keyword-conflict-simple-vars.out: keyword-conflict-simple-vars.in
	echo "----------- pyexpander without '-s'" > $@
	$(EXPANDER) -f $< >> $@ 2>&1
	echo "----------- pyexpander with '-s'" >> $@
	$(EXPANDER) -s -f $< >> $@ 2>&1

auto-continuation.out: auto-continuation.in
	echo "----------- pyexpander without '-a'" > $@
	$(EXPANDER) -f $< >> $@ 
	echo "----------- pyexpander with '-a'" >> $@
	$(EXPANDER) -a -f $< >> $@

macro-indent.out: macro-indent.in
	$(EXPANDER) -a -i -f $< > $@

ifeq "$(CREATE_TESTS)" "yes"
%.ok: %.out
	cp $< $@
endif

%.tst: %.in %.out %.ok
	diff $(wordlist 2, 3, $+)

#diff $(wordlist 2, 3, $+) || true

