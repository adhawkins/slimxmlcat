#!/usr/bin/python

import sys
import time
import codecs
import xml.dom

import SqueezeCenter.CLI.CLIComms

slim=SqueezeCenter.CLI.CLIComms.CLIComms("cube.gentlyhosting.co.uk",9001)

try:
	albums=slim.albums(10)
	
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
		artworkval=doc.createTextNode(str(album.artwork()))
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

		compilation=doc.createElement("artwork")
		compilationval=doc.createTextNode(str(album.artwork()))
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
			
			xmltracks.appendChild(xmltrack)
			
		xmlalbum.appendChild(xmltracks)

		docelement.appendChild(xmlalbum)


	fp = codecs.open("file.xml","w","UTF-8")
	doc.writexml(fp,"  ","  ","\n","UTF-8")
	#print doc.toxml("UTF-8")
		

except SqueezeCenter.CLI.CLIComms.CLICommsException, inst:
	print "Exception: " + inst.message()
	
  
