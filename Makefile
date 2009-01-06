VERSION=0.01

dist: .phony
	svn update && \
		mkdir -p slimxmlcat-$(VERSION) && \
		rsync -a --exclude "slimxmlcat-*" --exclude cursestest.py --exclude "*.xml" --exclude "*~" --exclude ".svn" --exclude "*.pyc" . slimxmlcat-$(VERSION) && \
		tar zcf slimxmlcat-$(VERSION).tar.gz slimxmlcat-$(VERSION) && \
		rm -rf slimxmlcat-$(VERSION)

clean: .phony
	rm -rf slimxmlcat-* *.tar.gz
	
.phony:
