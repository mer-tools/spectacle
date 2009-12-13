VERSION = 0.1
all:
dist:
	git tag v$(VERSION)
	git archive --format=tar --prefix=fastinit-$(VERSION)/ v$(VERSION) | \
		bzip2  > fastinit-$(VERSION).tar.bz2

