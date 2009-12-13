VERSION = 0.5
all:

tag: 
	git tag $(VERSION)
dist:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(VERSION) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

