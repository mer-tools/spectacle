VERSION = 0.2
all:

tag: 
	git tag v$(VERSION)
dist:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ $(VERSION) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

