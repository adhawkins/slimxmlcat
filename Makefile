VERSION=0.01

slimxmlcat-$(VERSION).tar.gz: dist

dist: .phony
	svn update && \
		mkdir -p slimxmlcat-$(VERSION) && \
		rsync -a --exclude "slimxmlcat-*" --exclude cursestest.py --exclude "*.xml" --exclude "*~" --exclude ".svn" --exclude "*.pyc" . slimxmlcat-$(VERSION) && \
		tar zcf slimxmlcat-$(VERSION).tar.gz slimxmlcat-$(VERSION) && \
		rm -rf slimxmlcat-$(VERSION)

install-webpages: slimxmlcat-$(VERSION).tar.gz
	mkdir -p /auto/gently-sw/slimxmlcat
	cp slimxmlcat-$(VERSION).tar.gz  /auto/gently-sw/slimxmlcat
	
clean: .phony
	rm -rf slimxmlcat-* *.tar.gz
	
.phony:
