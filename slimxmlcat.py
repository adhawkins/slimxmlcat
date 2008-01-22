#!/usr/bin/python

import sys
import time
import codecs
import optparse
import xml.dom

import SqueezeCenter.CLI.CLIComms

def progress(message):
	print message
	
def callback(processed,total):
	print "Processed " + str(processed) + " of " + str(total)
	
parser = optparse.OptionParser(version="%prog 1.0alpha",description="Retrieve album information from SqueezeCenter and generate an XML file for processing via XSLT")

parser.add_option("-s","--server",dest="server",help="SqueezeCenter host name or IP address",metavar="HOST",action="store",type="string",default="localhost")
parser.add_option("-c","--cliport",dest="cliport",help="SqueezeCenter CLI port",metavar="PORT",action="store",type="int",default=9001)
parser.add_option("-w","--httpport",dest="httpport",help="SqueezeCenter http port",metavar="PORT",action="store",type="int",default=9000)
parser.add_option("-l","--limit",dest="limit",help="Album limit",metavar="LIMIT",action="store",type="int",default=-1)
parser.add_option("-f","--file",dest="file",help="Output file name",metavar="FILE",action="store",type="string")
parser.add_option("-x","--xslt",dest="xsltfile",help="XSLT file name",metavar="FILE",action="store",type="string")

(options,args) = parser.parse_args()

if options.file==None:
	parser.print_help()
else:
	slim=SqueezeCenter.CLI.CLIComms.CLIComms(options.server,int(options.cliport),progress)

	try:
		albums=slim.albums(options.limit,callback)

		print "Found " + str(len(albums)) + " albums"

		doc=xml.dom.getDOMImplementation().createDocument("","catalogue",None)
		docelement=doc._get_documentElement()

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

			xmlalbum=doc.createElement("album");
			xmlalbum.setAttribute("id",album.id())

			name=doc.createElement("name")
			nameval=doc.createTextNode(album.name())
			name.appendChild(nameval)
			xmlalbum.appendChild(name)

			year=doc.createElement("year")
			yearval=doc.createTextNode(str(album.year()))
			year.appendChild(yearval)
			xmlalbum.appendChild(year)

			artwork=doc.createElement("artwork")
			artworkval=doc.createTextNode("http://" + options.server + ":" + str(options.httpport) + "/music/" + str(album.artwork()) + "/cover.jpg")
			artwork.appendChild(artworkval)
			xmlalbum.appendChild(artwork)

			disc=doc.createElement("disc")
			discval=doc.createTextNode(str(album.disc()))
			disc.appendChild(discval)
			xmlalbum.appendChild(disc)

			disccount=doc.createElement("disccount")
			disccountval=doc.createTextNode(str(album.disccount()))
			disccount.appendChild(disccountval)
			xmlalbum.appendChild(disccount)

			compilation=doc.createElement("compilation")
			compilationval=doc.createTextNode(str(album.compilation()))
			compilation.appendChild(compilationval)
			xmlalbum.appendChild(compilation)

			artist=doc.createElement("artist")
			artistval=doc.createTextNode(album.artist())
			artist.appendChild(artistval)
			xmlalbum.appendChild(artist)

			xmltracks=doc.createElement("tracks")

			tracks=album.tracks()

			for track in tracks:
				xmltrack=doc.createElement("track")
				xmltrack.setAttribute("number",str(track.tracknum()))

				title=doc.createElement("title")
				titleval=doc.createTextNode(track.title())
				title.appendChild(titleval)
				xmltrack.appendChild(title)

				duration=doc.createElement("duration")
				durationval=doc.createTextNode(str(track.duration()))
				duration.appendChild(durationval)
				xmltrack.appendChild(duration)

				artist=doc.createElement("artist")
				artistval=doc.createTextNode(track.artist())
				artist.appendChild(artistval)
				xmltrack.appendChild(artist)

				genre=doc.createElement("genre")
				genreval=doc.createTextNode(track.genre())
				genre.appendChild(genreval)
				xmltrack.appendChild(genre)

				xmltracks.appendChild(xmltrack)

			xmlalbum.appendChild(xmltracks)

			docelement.appendChild(xmlalbum)


		fp = codecs.open(str(options.file),"w","UTF-8")

		if options.xsltfile!=None:
			fp.write("<?xml-stylesheet type=\"text/xsl\" href=\"" + str(options.xsltfile) + "\"?>")

		doc.writexml(fp,"","","","UTF-8")


	except SqueezeCenter.CLI.CLIComms.CLICommsException, inst:
		print "Exception: " + inst.message()


