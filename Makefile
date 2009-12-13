VERSION = 0.1
all:

tag: 
	git tag v$(VERSION)
dist:
	git archive --format=tar --prefix=spectacle-$(VERSION)/ v$(VERSION) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

