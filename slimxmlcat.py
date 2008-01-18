#!/usr/bin/python

import SqueezeCenter.CLI.CLIComms
import time

slim=SqueezeCenter.CLI.CLIComms.CLIComms("localhost",9001)
albums=slim.albums()
print "Found " + str(len(albums)) + " albums"

for album in albums:
	print album.name() + " (" + album.year() + ") - " + album.artist() + " - " + album.artwork()
	
	tracks=album.tracks()
	
	for track in tracks:
		print "  " + repr(track.tracknum()).rjust(2) + ": " + track.title() + " - " + track.artist()
		
	time.sleep(1)
	print
	
	
