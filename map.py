from includes import sound_pool
mp=sound_pool.sound_pool()
class map:
	def __init__(self,minx,miny,maxx,maxy):
		self.x=0
		self.y=0
		self.minx=minx
		self.miny=miny
		self.maxx=maxx
		self.maxy=maxy
#	def zone(self,minx,maxx,miny,maxy,text):
#		
	def wall(self,wminx,wmaxx,wminy,wmaxy,wsound):
		if self.x==wminx:
			mp.play_stationary(wsound,False)
			self.x-=1