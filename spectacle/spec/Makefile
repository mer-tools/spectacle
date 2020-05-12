# ex: set tabstop=4 noexpandtab: 
PYTHON=python3
CHEETAH=cheetah
TEMPLATES=$(wildcard *.tmpl)
TEMPLATE_MODS=$(patsubst %.tmpl,%.py,$(TEMPLATES))
.SECONDARY: $(TEMPLATE_MODS)

all: $(TEMPLATE_MODS)

%.py: %.tmpl
	$(CHEETAH) compile --shbang="#!/usr/bin/env $(PYTHON)" --settings='useStackFrames=False' $<
	cp $@ __init__.py

clean:
	rm -f $(TEMPLATE_MODS)
	rm -f $(addsuffix .bak,$(TEMPLATE_MODS))
	rm -f *.xsd *.wsdl
	rm -f *.pyc *.pyo
	rm -f *.py
	rm -f *.bak
