VERSION = 0.1
all:
dist:
	git tag v$(VERSION)
	git archive --format=tar --prefix=spectacle-$(VERSION)/ v$(VERSION) | \
		bzip2  > spectacle-$(VERSION).tar.bz2

