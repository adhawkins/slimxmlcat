import socket 
import urllib
import sys

from SqueezeCenter.Database import Album
from SqueezeCenter.Database import Track

class CLICommsException(Exception):
	def __init__(self,message):
		self.__message=message

	def message(self):
		return self.__message

class CLIComms(object):
	def __init__(self,host,port):
		print "Connecting to " + host + ":" + str(port)
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect( (host, port))

	def __del__(self):
		print "Disconnecting"
		self.s.send('exit\n')
		self.s.close()

	def request(self, cmd):
		data = ""
		self.s.send(cmd + '\n')

#		print "Sent: " + cmd
		
		while (data.find("\n")==-1):
			data = data + self.s.recv(8192)

		if data.split()[0]!=cmd.split()[0]:
			raise CLICommsException("Unexpected response: Expected " + cmd.split()[0] + ", received " + data.split()[0])

#		print "Received: " + data
		
		return data.split()
  
	def tracks(self,album_id):
		tracks=list()
		thistrack=None

		response=self.request("titles 0 100 album_id:" + album_id + " tags:adtg")

		for item in response:
			splititem=urllib.unquote(item).split(":")

			if splititem[0]=="id":
				if thistrack!=None:
					tracks.append(thistrack)

				thistrack=Track.Track()
				thistrack.setid(splititem[1])
			elif splititem[0]=="title":
				thistrack.settitle(unicode(splititem[1],"utf-8"))
			elif splititem[0]=="tracknum":
				thistrack.settracknum(splititem[1])
			elif splititem[0]=="duration":
				thistrack.setduration(splititem[1])
			elif splititem[0]=="artist":
				thistrack.setartist(unicode(splititem[1],"utf-8"))
			elif splititem[0]=="genre":
				thistrack.setgenre(unicode(splititem[1],"utf-8"))
			elif splititem[0]=="rescan":
				raise CLICommsException("scan in progress - aborting")

		if thistrack!=None:
			tracks.append(thistrack)

		tracks.sort(lambda x, y: x.tracknum()-y.tracknum())
		
		return tracks

	def albums(self,limit=-1):
		albums=list()
		thisalbum=None

		numalbums=int(self.request("info total albums ?")[-1])
		if limit!=-1 and limit<numalbums:
			numalbums=limit

		print "Loading " + str(numalbums) + " albums"
		gotalbums=0
		numdots=0
		lastdots=0
		while (gotalbums<numalbums):
			response=self.request("albums " + str(gotalbums) + " 10 tags:lyjiqwa")
			for item in response:
				splititem=urllib.unquote(item).split(":")
				if splititem[0]=="id":

					if thisalbum!=None:
						albums.append(thisalbum)

						thisalbum=None
						gotalbums=gotalbums+1
						
						if gotalbums==numalbums:
							break;

					thisalbum=Album.Album()
					thisalbum.setid(splititem[1])
					
					numdots=int(float(gotalbums)/float(numalbums)*40.0)
					
					if numdots!=lastdots:
						for dot in range(lastdots,numdots):
							print ".",
							
					sys.stdout.flush()
					lastdots=numdots

					tracks=self.tracks(splititem[1])
					thisalbum.settracks(tracks)
				elif splititem[0]=="album":
					thisalbum.setname(unicode(splititem[1],"utf-8"))
				elif splititem[0]=="year":
					thisalbum.setyear(splititem[1])
				elif splititem[0]=="artwork_track_id":
					thisalbum.setartwork(splititem[1])
				elif splititem[0]=="disc":
					thisalbum.setdisc(splititem[1])
				elif splititem[0]=="disccount":
					thisalbum.setdisccount(splititem[1])
				elif splititem[0]=="compilation":
					thisalbum.setcompilation(splititem[1])
				elif splititem[0]=="artist":
					thisalbum.setartist(unicode(splititem[1],"utf-8"))
				elif splititem[0]=="rescan":
					raise CLICommsException("scan in progress - aborting")

			if thisalbum!=None:
				albums.append(thisalbum)

				thisalbum=None
				gotalbums=gotalbums+1

				if gotalbums==numalbums:
					break;

		print

		return albums
    