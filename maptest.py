import sys
import pygame
from random import randint,choice
import map
from includes import sound, sound_pool as p,output,keyboard,timer,window
errors = open("errors.log","a")
sys.stderr = errors
objs = []
objhorns = ["beep"]
s=sound.sound()
s.load("s/obj_ultrasmash_buildup.ogg")
amb=sound.sound()
amb.load("s/amb.ogg")
walktime=timer.Timer()
airtimer=timer.Timer()
jumptimer=timer.Timer()
jumptime = 90
falltimer=timer.Timer()
falling = False
falltime = 120
fall_counter = 0
jump_counter = 0
jump_height = 5
jumping = False
rising = False
lowering = False
deathwhoosh=True
m=map.map(0,0,30,30)
def shift_is_down():
	return window.key_down(pygame.K_LSHIFT) or window.key_down(pygame.K_RSHIFT)
def playstep():
	if m.y == 0: p.p.play_stationary("s/step"+str(randint(1,5))+".ogg", False)
def main():
	global jumping,rising,jumptimer,falltimer,lowering,falltime,jump_counter,jumptime,deathwhoosh
	walkspeed=140
	airtime=walkspeed-20
	window.show_window("map")
	amb.play_looped()
	while True:
		window.process_events()
		gravity()
		objscheck()
		if window.key_pressed(pygame.K_PAGEUP) and walkspeed>=10:
			walkspeed-=10
			output.speak("Speed: "+str(walkspeed)+" ms.")
		if window.key_pressed(pygame.K_PAGEDOWN) and walkspeed<=2000:
			walkspeed+=10
			output.speak("Speed: "+str(walkspeed)+" ms")
		if window.key_down(pygame.K_RIGHT) and m.x < m.maxx and walktime.elapsed>=walkspeed:
			walktime.restart()
			m.x+=1
			p.p.update_listener_2d(m.x,m.y)
			playstep()
		if window.key_down(pygame.K_r) and walktime.elapsed>=walkspeed and not jumping:
			m.y+=1
			walktime.restart()
		if window.key_down(pygame.K_f) and walktime.elapsed>=walkspeed and m.y>0 and not jumping and not falling and not rising:
			m.y-=1
			walktime.restart()
			if m.y==0:
				playstep()
		if window.key_down(pygame.K_UP) and not jumping and not falling and not rising and not lowering and m.y<1:
			p.p.play_stationary("s/jump.ogg",False)
			jumping = True
			rising = True
		if window.key_down(pygame.K_LEFT) and walktime.elapsed>=walkspeed and m.x > m.minx:
			walktime.restart()
			m.x-=1
			p.p.update_listener_2d(m.x,m.y)
			playstep()
		if window.key_pressed(pygame.K_c):
			output.speak(f"Coordinates {m.x}, {m.y}")
		if window.key_pressed(pygame.K_w):
			if deathwhoosh==True:
				deathwhoosh=False
				output.speak("Death whoosh off.")
			else:
				deathwhoosh=True
				output.speak("Death whoosh on.")

		if window.key_pressed(pygame.K_BACKSPACE):
			ultrasmash()
		if window.key_pressed(pygame.K_SPACE):
			spawn_object()
		if window.key_pressed(pygame.K_o):
			output.speak(f"{str(len(objs))} objects")
		if window.key_pressed(pygame.K_f) and m.y>0: m.y-=1
		if window.key_pressed(pygame.K_ESCAPE):
			sys.exit()
def gravity():
	global jumping,rising,jumptimer,falltimer,lowering,falltime,jump_counter,jumptime
	if jumping:
		if rising and jump_counter < jump_height and jumptimer.elapsed > jumptime:
			jumptimer.restart()
			jump_counter += 1
			m.y += 1
		if jump_counter >= jump_height:
			rising = False
			lowering = True
		if lowering and m.y > 0 and falltimer.elapsed > falltime:
			falltimer.restart()
			jump_counter -= 1
			m.y -= 1
			if m.y == 0:
				p.p.play_stationary("s/land.ogg",False)
				rising= False
				lowering = False
				jumping = False
class obj:
	def __init__(self,x=0,y=0):
		self.remove = False
		self.x = x
		self.y = y
		self.horn_type = choice(objhorns)
		self.beepstarttimer = timer.Timer()
		self.beependtimer = timer.Timer()
		self.beepstarttime = randint(100,5000)
		self.beependtime = randint(100,1000)
		self.beeping = False
		self.movetimer=timer.Timer()
		self.movetime = randint(75,400)
		self.pitch = randint(75,200)
		self.loop = p.p.play_extended_2d(f"s/obj{randint(1,7)}.ogg",m.x,m.y,self.x,0,0,0,0,0,True,0,0,0,self.pitch)
		self.tiresloop = None
		self.beeploop = None
		if self.movetime >= 300:
			self.tiresloop = p.p.play_2d("s/objtires2.ogg",m.x,m.y,self.x,self.y,True)
		elif self.movetime >= 150:
			self.tiresloop = p.p.play_2d("s/objtires1.ogg",m.x,m.y,self.x,self.y,True)
		else:
			self.tiresloop = p.p.play_2d("s/objtires3.ogg",m.x,m.y,self.x,self.y,True)
		if self.horn_type == "beeeeeeeeeep":
			self.beeploop = p.p.play_extended_2d("s/horn.ogg",m.x,m.y,self.x,0,0,0,0,0,True,0,0,0,self.pitch)
	def act(self):
		if self.movetimer.elapsed > self.movetime:
			self.movetimer.restart()
			self.x += 1
			p.p.update_sound_2d(self.loop,self.x,self.y)
			p.p.update_sound_2d(self.tiresloop,self.x,self.y)
			if self.beeploop: p.p.update_sound_2d(self.beeploop,self.x,self.y)
		if self.horn_type == "beep" and self.beeping and self.beependtimer.elapsed > self.beependtime:
			self.beependtimer.restart()
			self.beependtime = randint(100,1000)
			self.beepstarttimer.restart()
			if self.beeploop: p.p.destroy_sound(self.beeploop)
			self.beeping = False
		if self.horn_type == "beep" and not self.beeping and self.beepstarttimer.elapsed > self.beepstarttime:
			self.beepstarttimer.restart()
			self.beepstarttime = randint(100,5000)
			self.beependtimer.restart()
			self.beeploop = p.p.play_extended_2d("s/horn.ogg",m.x,m.y,self.x,0,0,0,0,0,True,0,0,0,self.pitch)
			self.beeping = True
		if self.x == m.maxx:
			if self.x<=m.maxx:
				if deathwhoosh==True: p.p.play_stationary("s/objdeath.ogg",False)
			p.p.play_2d("s/objsmash.ogg",m.x,m.y,self.x,self.y,False)
			self.remove = True
def objscheck():
	for i in objs:
		if i.remove:
			p.p.destroy_sound(i.loop)
			p.p.destroy_sound(i.tiresloop)
			if i.beeploop: p.p.destroy_sound(i.beeploop)
			spawn_object(randint(-100,-50))
			objs.remove(i)
		else: i.act()
def ultrasmash():
	if len(objs)==0:
		output.speak("No objects.")
	else:
		s.play_wait()
		for sm in objs:
			p.p.play_extended_2d("s/obj_ultrasmash.ogg",m.x,m.y,sm.x,0,0,0,0,0,False,0,0,0,sm.pitch)
			if sm.loop: p.p.destroy_sound(sm.loop)
			if sm.tiresloop: p.p.destroy_sound(sm.tiresloop)
			if sm.beeploop: p.p.destroy_sound(sm.beeploop)
	objs.clear()
def spawn_object(x=0,y=0):
	objs.append(obj(x,y))
if __name__=="__main__":
	main()