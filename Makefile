VERSION = $(shell cat VERSION)
TAGVER = $(shell cat VERSION | sed -e "s/\([0-9\.]*\).*/\1/")

ifeq ($(VERSION), $(TAGVER))
	TAG = $(TAGVER)
else
	TAG = "HEAD"
endif

all: tmpls
	python setup.py build

tmpls:
	cd spectacle/spec; $(MAKE)
	cd spectacle/dsc; $(MAKE)

tag:
	git tag $(VERSION)

dist-bz2:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(TAG) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

dist-gz:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(TAG) | \
		gzip  > spectacle-$(VERSION).tar.gz

doc:
	markdown README > README.html

test:
	cd tests/; python alltest.py

install: all install-data
	python setup.py install

install-data:
	install -d ${DESTDIR}/usr/share/spectacle/
	install -m 644 data/*csv ${DESTDIR}/usr/share/spectacle/
	install -m 644 data/GROUPS ${DESTDIR}/usr/share/spectacle/

clean:
	rm -rf build/
	rm -f README.html
	cd spectacle/spec; $(MAKE) clean
	cd spectacle/dsc; $(MAKE) clean
