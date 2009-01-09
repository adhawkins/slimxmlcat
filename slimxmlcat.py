#!/usr/bin/python

import sys
import time
import codecs
import optparse
import libxml2
import libxslt

import SqueezeCenter.CLI.CLIComms

def progress(message):
	print message
	
def callback(processed,total):
	print "Processed " + str(processed) + " of " + str(total)
	
parser = optparse.OptionParser(version="%prog 0.01",description="Retrieve album information from SqueezeCenter and generate an XML file for processing via XSLT")

parser.add_option("-s","--server",dest="server",help="SqueezeCenter host name or IP address",metavar="HOST",action="store",type="string",default="localhost")
parser.add_option("-c","--cliport",dest="cliport",help="SqueezeCenter CLI port",metavar="PORT",action="store",type="int",default=9001)
parser.add_option("-w","--httpport",dest="httpport",help="SqueezeCenter http port",metavar="PORT",action="store",type="int",default=9000)
parser.add_option("-l","--limit",dest="limit",help="Album limit",metavar="LIMIT",action="store",type="int",default=-1)
parser.add_option("-f","--file",dest="file",help="Output file name",metavar="FILE",action="store",type="string")
parser.add_option("-x","--xslt",dest="xsltfile",help="XSLT file name",metavar="FILE",action="store",type="string")

(options,args) = parser.parse_args()

if options.file==None or options.xsltfile==None:
	parser.print_help()
else:
	slim=SqueezeCenter.CLI.CLIComms.CLIComms(options.server,int(options.cliport),progress)

	try:
		albums=slim.albums(options.limit,callback)

		print "Found " + str(len(albums)) + " albums"

		doc=libxml2.newDoc("1.0")
		root = libxml2.newNode("catalogue")
		doc.setRootElement(root)

		numdots=0
		lastdots=0
		processedalbums=0

		for album in albums:
			processedalbums=processedalbums+1

			numdots=int(float(processedalbums)/float(len(albums))*40.0)
			if numdots!=lastdots:
				for dot in range(lastdots,numdots):
					print ".",

			sys.stdout.flush()
			lastdots=numdots

			xmlalbum=root.newChild(None, "album", None)
			xmlalbum.newProp("id",album.id())
			
			xmlalbum.newTextChild(None, "name", album.name().encode("utf-8"))
			xmlalbum.newTextChild(None, "year", str(album.year()))
			xmlalbum.newTextChild(None, "artwork", "http://" + options.server + ":" + str(options.httpport) + "/music/" + str(album.artwork()) + "/cover.jpg")
			xmlalbum.newTextChild(None, "disc", str(album.disc()))
			xmlalbum.newTextChild(None, "disccount", str(album.disccount()))
			xmlalbum.newTextChild(None, "compilation", str(album.compilation()))
			xmlalbum.newTextChild(None, "artist", album.artist().encode("utf-8"))
			
			xmltracks=xmlalbum.newChild(None, "tracks", None)
			tracks=album.tracks()

			for track in tracks:
				xmltrack=xmltracks.newChild(None, "track", None)
				
				if track.discnum()!=0:
					xmltrack.newProp("number",str(track.discnum()) + " - " + str(track.tracknum()))
				else:
					xmltrack.newProp("number",str(track.tracknum()))

				xmltrack.newChild(None, "title", track.title().encode("utf-8"))
				xmltrack.newTextChild(None, "duration", str(track.duration()/60) + ":" + str(track.duration()%60).zfill(2))
				xmltrack.newTextChild(None, "artist", track.artist().encode("utf-8"))
				xmltrack.newTextChild(None, "genre", track.genre().encode("utf-8"))

		doc.saveFormatFileEnc(options.file+".xml","utf-8",1);

		if options.xsltfile!=None:
			styledoc = libxml2.parseFile(options.xsltfile)
			style = libxslt.parseStylesheetDoc(styledoc)
			result = style.applyStylesheet(doc, None)
			style.saveResultToFilename(options.file, result, 0)
			style.freeStylesheet()
			doc.freeDoc()
			result.freeDoc()	
	
	except SqueezeCenter.CLI.CLIComms.CLICommsException, inst:
		print "Exception: " + inst.message()
