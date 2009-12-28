VERSION = 0.5
all:
	cd spectacle/spec; $(MAKE)
	cd spectacle/dsc; $(MAKE)
	python setup.py build

tag: 
	git tag $(VERSION)
dist:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(VERSION) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

install: all
	python setup.py install
