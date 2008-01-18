import socket 
import urllib
import sys

from SqueezeCenter.Database import Album
from SqueezeCenter.Database import Track

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
		
		while (data.find("\n")==-1):
			data = data + self.s.recv(8192)
			
		return data

	def albums(self):
		retalbums=list()
		thisalbum=None
		numalbums=int(self.request("info total albums ?").split()[-1])
		gotalbums=0
		numdots=0
		lastdots=0
		while (gotalbums<numalbums):
			response=self.request("albums " + str(gotalbums) + " 10 tags:lyjiqwa").split()
			for item in response:
				splititem=urllib.unquote(item).split(":")
				if splititem[0]=="id":
					if thisalbum!=None:
						retalbums.append(thisalbum)
						
					thisalbum=Album.Album()
					thisalbum.setid(splititem[1])
					gotalbums=gotalbums+1
		
					numdots=int(float(gotalbums)/float(numalbums)*40.0)
					if numdots!=lastdots:
						print ".",
						sys.stdout.flush()
						lastdots=numdots
						
					tracks=list()
					thistrack=None
					
					trackresponse=self.request("titles 0 100 album_id:" + thisalbum.id() + " tags:adt").split()
					
					for trackitem in trackresponse:
						splittrackitem=urllib.unquote(trackitem).split(":")
						
						if splittrackitem[0]=="id":
							if thistrack!=None:
								tracks.append(thistrack)
								
							thistrack=Track.Track()
							thistrack.setid(splittrackitem[1])
						elif splittrackitem[0]=="title":
							thistrack.settitle(splittrackitem[1])
						elif splittrackitem[0]=="tracknum":
							thistrack.settracknum(splittrackitem[1])
						elif splittrackitem[0]=="duration":
							thistrack.setduration(splittrackitem[1])
						elif splittrackitem[0]=="artist":
							thistrack.setartist(splittrackitem[1])
					
					if thistrack!=None:
						tracks.append(thistrack)

					tracks.sort(lambda x, y: x.tracknum()-y.tracknum())
					thisalbum.settracks(tracks)
				elif splititem[0]=="album":
					thisalbum.setname(splititem[1])
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
					thisalbum.setartist(splititem[1])

		if thisalbum!=None:
			retalbums.append(thisalbum)
		
		print
		
		return retalbums
		