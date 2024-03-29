class Track(object):
	def __init__(self):
		self.__id=0
		self.__title=""
		self.__tracknum=0
		self.__duration=0.0
		self.__artist=""
		self.__genre=""
		self.__discnum=0

	def setid(self,id):
		self.__id=id
		
	def settitle(self,title):
		self.__title=title

	def settracknum(self,tracknum):
		self.__tracknum=int(tracknum)
		
	def setduration(self,duration):
		self.__duration=int(float(duration))
		
	def setartist(self,artist):
		self.__artist=artist

	def setgenre(self,genre):
		self.__genre=genre
	
	def setdiscnum(self,discnum):
		self.__discnum=int(discnum)
		
	def id(self):
		return self.__id
		
	def title(self):
		return self.__title
		
	def tracknum(self):
		return self.__tracknum
		
	def duration(self):
		return self.__duration
		
	def artist(self):
		return self.__artist

	def genre(self):
		return self.__genre
		
	def discnum(self):
		return self.__discnum
