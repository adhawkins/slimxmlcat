import libxml2
import libxslt

styledoc = libxml2.parseFile("sample2.xsl")
style = libxslt.parseStylesheetDoc(styledoc)
doc = libxml2.parseFile("test/test.xml")
result = style.applyStylesheet(doc, None)
style.saveResultToFilename("test/test.html", result, 0)
style.freeStylesheet()
doc.freeDoc()
result.freeDoc()