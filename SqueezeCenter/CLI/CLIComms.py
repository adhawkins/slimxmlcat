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
	__message=None
	def __init__(self,host,port,message=None):
		self.__message=message
		
		if (self.__message!=None):
			self.__message("Connecting to " + host + ":" + str(port))
			
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect( (host, port))

	def __del__(self):
		if (self.__message!=None):
			self.__message("Disconnecting")
			
		self.s.send('exit\n')
		self.s.close()

	def request(self, cmd):
		data = ""
		self.s.send(cmd + '\n')

		while (data.find("\n")==-1):
			data = data + self.s.recv(8192)

		if data.split()[0]!=cmd.split()[0]:
			raise CLICommsException("Unexpected response: Expected " + cmd.split()[0] + ", received " + data.split()[0])

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

	def albums(self,limit=-1,callback=None):
		albums=list()
		thisalbum=None

		numalbums=int(self.request("info total albums ?")[-1])
		if limit!=-1 and limit<numalbums:
			numalbums=limit

		if (self.__message!=None):
			self.__message("Loading " + str(numalbums) + " albums")
			
		while (len(albums)<numalbums):
			response=self.request("albums " + str(len(albums)) + " 10 tags:lyjiqwa")
			for item in response:
				splititem=urllib.unquote(item).split(":")
				if splititem[0]=="id":

					if thisalbum!=None:
						albums.append(thisalbum)
						if callback!=None:
							callback(len(albums),numalbums)

						thisalbum=None
						
						if len(albums)==numalbums:
							break;

					thisalbum=Album.Album()
					thisalbum.setid(splititem[1])
					
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
				if callback!=None:
					callback(len(albums),numalbums)

				thisalbum=None

				if len(albums)==numalbums:
					break;

		return albums
    