class Album(object):
	def __init__(self):
		self.__id=0
		self.__name=""
		self.__year=0
		self.__artwork=""
		self.__disc=0
		self.__disccount=0
		self.__compilation=0
		self.__artist=""
		self.__tracks=list()
	
	def setid(self,id):
		self.__id=id
		
	def setname(self,newname):
		self.__name=newname
		
	def setyear(self,year):
		self.__year=int(year)
		
	def setartwork(self,artwork):
		self.__artwork=artwork
		
	def setdisc(self,disc):
		self.__disc=disc
		
	def setdisccount(self,disccount):
		self.__disccount=disccount
		
	def setcompilation(self,compilation):
		self.__compilation=compilation
		
	def setartist(self,artist):
		self.__artist=artist
		
	def settracks(self,tracks):
		self.__tracks=tracks
		
	def id(self):
		return self.__id
		
	def name(self):
		return self.__name
		
	def year(self):
		return self.__year
		
	def artwork(self):
		return self.__artwork

	def disc(self):
		return self.__disc
		
	def disccount(self):
		return self.__disccount
		
	def compilation(self):
		return self.__compilation
		
	def artist(self):
		return self.__artist
		
	def tracks(self):
		return self.__tracks