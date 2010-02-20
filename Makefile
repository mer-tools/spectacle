VERSION = $(shell cat VERSION)

all:
	cd spectacle/spec; $(MAKE)
	cd spectacle/dsc; $(MAKE)
	python setup.py build

tag: 
	git tag $(VERSION)

dist-bz2:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(VERSION) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

dist-gz:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(VERSION) | \
		gzip  > spectacle-$(VERSION).tar.gz

doc:
	markdown README > README.html

install: all
	python setup.py install
