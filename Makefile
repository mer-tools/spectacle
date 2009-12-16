VERSION = 0.4
all:

tag: 
	git tag $(VERSION)
dist:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(VERSION) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

install:
	cd spectacle/spec; $(MAKE)
	cd spectacle/dsc; $(MAKE)
	python setup.py install
