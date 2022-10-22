from . import window
from . import timer
import pygame

key_holds=[]

class key_hold(object):
	def __init__(self, _key_code, _delay, _repeat):
		self.status=False
		self.key_flag=0
		self.key_code=_key_code
		self.delay=_delay
		self.repeat=_repeat
		self.repeat_time=self.delay
		self.key_timer=timer.Timer()

	def pressing(self):
		self.status=window.key_down(self.key_code)
		if self.status==False:
			self.repeat_time=0
			self.key_timer.restart()
			self.key_flag=0
			return False
		if self.key_timer.elapsed>=self.repeat_time:
			if self.key_flag==0:
				self.key_flag=1
				self.repeat_time=self.delay
				self.key_timer.restart()
			elif self.key_flag==1:
				self.repeat_time=self.repeat
				self.key_timer.restart()
			return True
		return False

def key_holding(key, delay=500, repeat=50):
	for i in key_holds:
		if i.key_code==key:
			return i.pressing()
	key_holds.append(key_hold(key, delay, repeat))
	for i in key_holds:
		if i.key_code==key:
			return i.pressing()
