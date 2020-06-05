from simulator import get_sensors, move_forward, move_backward, turn_left, turn_right, submit, set_map
# DO NOT MODIFY LINE 1
# You may import any libraries you want. But you may not import simulator_hidden

# Colors
black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)
blue = (0,180,255)

##############################
#### Write your code here ####
##############################
def add(a,b):
	return ((a[0]+b[0],a[1]+b[1]))

N=(0,-1)
E=(1,0)
S=(0,1)
W=(-1,0)
lakes=[]
buildings=[]	

set_map((15,10),[(11, 0), (5, 0), (9, 2), (10, 3), (11, 2), (1, 0), (1, 7), (12, 0), (5, 3), (3, 9), (13, 6), (4, 6), (0, 5), (1, 5), (5, 8), (7, 3), (2, 3), (1, 9), (13, 4), (7, 5)],[(5, 1), (12, 8), (6, 8), (6, 7), (0, 3), (7, 6), (14, 2), (13, 1), (5, 9), (3, 2), (12, 6), (1, 8), (0, 1), (12, 7), (14, 8), (8, 1), (12, 1), (14, 5), (5, 2), (0, 9)])
q1=0
q2=0
q3=0
while get_sensors()[0][1]!=gray:
	move_forward()
	q1+=1

a1=0
a2=0
while get_sensors()[0][0]==get_sensors()[0][1]:
	turn_left()
	a2+=1
while get_sensors()[0][0]!=get_sensors()[0][1]:
	turn_left()	
	a1+=1
while get_sensors()[0][0]==get_sensors()[0][1]:
	turn_left()
	a1+=1
while get_sensors()[0][0]!=get_sensors()[0][1]:
	turn_left()
	a1+=1
turn_left(a2-1)
a=a1+a2+a2-1
av=int(a/2)

b=0
if not -1<get_sensors()[1]<4:
	turn_left(int(av))
	while get_sensors()[0][1]!=gray:
		move_backward()
		q2+=1
	while get_sensors()[0][1]!=white and get_sensors()[0][1]!=blue:
		move_backward()
		q2+=1
	move_forward()
	q2-=1
	while get_sensors()[0][1]!=white and get_sensors()[0][1]!=blue:
		move_forward()
		b+=1
	while get_sensors()[0][1]!=black:
		move_forward()
		b+=1
	move_backward(b-q1-q2)
	turn_right(int(av))
else:
	turn_right(int(av/2))
	while get_sensors()[0][1]!=gray:
		move_backward()
		q3+=1
	while get_sensors()[0][1]!=white and get_sensors()[0][1]!=blue:
		move_backward()
		q3+=1
	move_forward()
	q3-=1
	while get_sensors()[0][1]!=white and get_sensors()[0][1]!=blue:
		move_forward()
		b+=1
	while get_sensors()[0][1]!=black:
		move_forward()
		b+=1
	move_backward(b-q3)
	turn_left(int(av/2))
	move_backward(q1)

mv=b





class robot() :
	def __init__(self,mv,av,pos=(0,0),dir=S,end=0,history=[(0,0)],mapend=0):
		self.mv = mv
		self.av = av
		self.pos = pos
		self.dir = dir
		self.end = end
		self.history = history
		self.mapend = mapend

	def seeright(self) :
		turn_right(int(self.av/2))
		if self.dir == E:
			self.dir = S
		elif self.dir == S:
			self.dir = W
		elif self.dir == W:
			self.dir = N
		elif self.dir == N:
			self.dir = E

	def seeleft(self) :
		turn_left(int(self.av/2))
		if self.dir == E:
			self.dir = N
		elif self.dir== N:
			self.dir = W
		elif self.dir == W:
			self.dir = S
		elif self.dir == S:
			self.dir = E
	def seeEast(self) :
		if self.dir==W:
			self.seeback()
		elif self.dir == N:
			self.seeright()
		elif self.dir == S:
			self.seeleft()
		elif self.dir == E:
			return
	def seeWest(self):
		if self.dir==E:
			self.seeback()
		elif self.dir == N:
			self.seeleft()
		elif self.dir == S:
			self.seeright()
		elif self.dir == W:
			return

	def seeback(self) :
		if self.dir == S or self.dir == E:
			self.seeleft()
			self.seeleft()
		else:
			self.seeright()
			self.seeright()

	def move(self):
		for i in range(self.mv):
			move_forward()
			if get_sensors()[0][1]==black:
				if self.dir==E:
					self.mapend=self.pos[0]
				move_backward(i+1)
				self.end=max(self.end,self.pos[1])
				return False
		if get_sensors()[0][1] == blue and add(self.pos,self.dir) not in lakes:
			lakes.append(add(self.pos,self.dir))
		self.pos=add(self.pos,self.dir)
		if self.pos not in self.history:
			self.history.append(self.pos)
		return True

	def obstacle(self):
		if -1<get_sensors()[1]<=4 :
			if add(self.pos,self.dir) not in buildings:
				buildings.append(add(self.pos,self.dir))
				self.end=max(self.end,add(self.pos,self.dir)[1])
			return True
		else:
			False

	def before(self):
		if self.dir == N:
			return (self.pos[0]-1,self.pos[1]) in buildings or (self.pos[0]-1,self.pos[1]-1) in buildings or (self.pos[0]-1,self.pos[1]-2) in buildings
		elif self.dir == S:
			return (self.pos[0]-1,self.pos[1]) in buildings or (self.pos[0]-1,self.pos[1]+1) in buildings or (self.pos[0]-1,self.pos[1]+2) in buildings
		else:
			False

	def check(self):
		#case 1-0
		if self.dir == S and self.pos[0]==0:
			self.seeleft()
			#case 1-1
			if self.obstacle():
				self.seeleft()
				self.move()
				self.seeright()
				self.move()
				self.move()
				self.seeright()
				self.move()
				self.move()
				self.seeright()
				self.move()
				self.seeleft()
				#case 1-1-1
				if self.move()==False:
					self.seeback()
					return
				self.seeright()
				self.move()
				self.seeleft()
				return
			self.move()
			self.seeright()
			#case 1-2
			if self.obstacle():
				self.seeleft()
				self.move()
				self.seeright()
				self.move()
				#case 1-2-1
				if self.move()==False:
					self.seeback()
					self.move()
					self.seeleft()
					self.move()
					self.seeright()
					return
				self.seeright()
				self.move()
				self.move()
				self.seeleft()
				return
			self.move()
			#case 1-3
			if self.obstacle():
				self.seeleft()
				self.move()
				self.seeright()
				self.move()
				#case 1-3-1
				if self.move()==False:
					self.seeback()
					self.move()
					self.seeleft()
					self.move()
					self.seeright()
					return
				self.seeright()
				self.move()
				self.move()
				self.seeright()
				self.move()
				self.seeback()
				return
			#case 1-0-1
			if self.move()==False:
				self.seeback()
				return
			self.seeright()
			#case 1-4
			if self.obstacle():
				self.seeleft()
				#case 1-4-1
				if self.move()==False:
					self.seeback()
					return
				self.seeright()
				self.move()
				self.seeleft()
				return
			self.move()
			self.seeleft()
			return
		#case 2
		if self.dir == S and self.pos[0]!=0:
			#case 2-1
			if not self.before():
				#case 2-1-0
				if self.pos[1]==self.end-1:
					self.seeleft()
					#case 2-1-1
					if self.obstacle():
						self.seeleft()
						self.move()
						self.seeright()
						self.move()
						self.seeleft()
						return
					#case 2-1-0-1
					if self.move() == False:
						self.seeleft()
						return
					self.seeright()
					#case 2-1-2
					if self.obstacle():
						self.seeleft()
						self.seeleft()
						return
					self.move()
					self.seeback()
					return
				self.seeright()
				self.move()
				self.seeleft()
				self.move()
				self.move()
				self.seeleft()
				#case 2-1-3
				if self.obstacle():
					self.seeright()
					#case 2-1-3-1
					if self.move()==False:
						self.seeback()
						self.move()
						self.move()
						self.seeright()
						self.move()
						#case 2-1-3-2
						if self.move()==False:
							self.seeleft()
							return
						self.seeright()
						self.move()
						self.move()
						self.seeback()
						return
					self.seeleft()
					self.move()
					self.seeright()
					return
				self.move()
				self.seeright()
				return
			#case 2-2
			if self.before() :
				self.seeleft()
				if self.move()==False:
					#case 2-3-0,2-4-0,2-2-0-1
					if self.pos[1] == self.end - 1:
						self.seeleft()
						return
					self.seeright()
					self.seeright()
					#case 2-3
					if self.obstacle():
						self.seeright()
						self.move()
						self.seeleft()
						self.move()
						self.move()
						self.seeleft()
						self.move()
						self.move()
						self.seeleft()
						self.move()
						self.seeright()
						self.move()
						self.seeleft()
						self.move()
						self.seeright()
						return
					self.move()
					self.seeleft()
					#case 2-4
					if self.obstacle():
						self.seeright()
						self.move()
						self.seeleft()
						self.move()
						self.move()
						self.seeleft()
						self.move()
						self.move()
						self.seeright()
						return
					self.move()
					#case 2-5
					if self.obstacle():
						self.seeright()
						self.move()
						self.seeleft()
						self.move()
						if self.move() == False:
							return
						self.seeleft()
						self.move()
						self.move()
						self.seeleft()
						self.move()
						self.seeright()
						self.seeright()
						return
					return
				self.seeright()
				self.seeright()
				self.move()
				self.seeleft()
				#case 2-2-0
				if self.pos[1]==self.end-1:
					self.seeleft()
					#case 2-2-1
					if self.obstacle():
						self.seeleft()
						self.move()
						self.seeright()
						self.move()
						self.seeleft()
						return
					self.move()
					self.seeright()
					#case 2-2-2
					if self.obstacle():
						self.seeleft()
						self.seeleft()
						return
					self.move()
					self.seeback()
					return
				self.seeleft()
				self.move()
				self.seeright()
				self.move()
				self.move()
				self.seeright()
				#case 2-2-3
				if self.obstacle():
					self.seeleft()
					#case 2-2-3-1
					if self.move()==False:
						self.seeback()
						return
					self.seeright()
					self.move()
					self.seeleft()
					return
				self.move()
				self.seeleft()
				return
		#case 3
		if self.dir == N and self.pos[0]!=0:
			#case 3-1
			if not self.before():
				#case 3-1-0
				if self.pos[1]==1:
					self.seeright()
					#case 3-1-1
					if self.obstacle():
						self.seeright()
						self.move()
						self.seeleft()
						self.move()
						self.seeright()
						return
					#case 3-1-0-1
					if self.move() == False:
						self.seeright()
						return
					self.seeleft()
					#case 3-1-2
					if self.obstacle():
						self.seeright()
						self.seeright
						return
					self.move()
					self.seeback()
					return
				self.seeleft()
				self.move()
				self.seeright()
				self.move()
				self.move()
				self.seeright()
				#case 3-1-3
				if self.obstacle():
					self.seeleft()
					#case 3-1-3-1
					if self.move()==False:
						self.seeback()
						self.move()
						self.move()
						self.seeleft()
						self.move()
						#case 3-1-3-2
						if self.move()==False:
							self.seeleft()
							return
						self.seeleft()
						self.move()
						self.move()
						self.seeback()
						return
					self.seeright()
					self.move()
					self.seeleft()
					return
				self.move()
				self.seeleft()
				return
			#case 3-2
			if self.before() :
				self.seeright()
				if self.move() == False:
					#case 3-3-0,3-4-0,3-2-0-1
					if self.pos[1] == 1:
						self.seeleft()
						return
					self.seeleft()
					self.seeleft()
					#case 3-3
					if self.obstacle():
						self.seeleft()
						self.move()
						self.seeright()
						self.move()
						self.move()
						self.seeright()
						self.move()
						self.move()
						self.seeright()
						self.move()
						self.seeleft()
						self.move()
						self.seeright()
						self.move()
						self.seeleft()
						return
					self.move()
					self.seeright()
					#case 3-4
					if self.obstacle():
						self.seeleft()
						self.move()
						self.seeright()
						self.move()
						self.move()
						self.seeright()
						self.move()
						self.move()
						self.seeleft()
						return
					self.move()
					#case 3-5
					if self.obstacle():
						self.seeleft()
						self.move()
						self.seeright()
						self.move()
						if self.move() == False:
							return
						self.seeright()
						self.move()
						self.move()
						self.seeright()
						self.move()
						self.seeleft()
						self.seeleft()
						return
					return
				self.seeleft()
				self.seeleft()
				self.move()
				self.seeright()
				#case 3-2-0
				if self.pos[1]==1:
					self.seeright()
					#case 3-2-1
					if self.obstacle():
						self.seeright()
						self.move()
						self.seeleft()
						self.move()
						self.seeright()
						return
					self.move()
					self.seeleft()
					#case 3-2-2
					if self.obstacle():
						self.seeright()
						self.seeright()
						return
					self.move()
					self.seeback()
					return
				self.seeright()
				self.move()
				self.seeleft()
				self.move()
				self.move()
				self.seeleft()
				#case 3-2-3
				if self.obstacle():
					self.seeright()
					#case 3-2-3-1
					if self.move()==False:
						self.seeback()
						return
					self.seeleft()
					self.move()
					self.seeright()
					return
				self.move()
				self.seeright()
				return

	def check2(self):
		if self.pos[1]==0 and self.dir==E:
			if self.obstacle():
				self.seeright()
				self.move()
				self.seeleft()
				if self.obstacle():
					self.seeright()
					self.move()
					self.seeleft()
					self.move()
					self.seeright()
					return
				self.move()
				self.seeright()
				return
		if self.pos[1]==self.end and self.dir==E:
			if self.obstacle():
				self.seeleft()
				self.move()
				self.seeright()
				if self.obstacle():
					self.seeleft()
					self.move()
					self.seeright()
					self.move()
					self.seeleft()
					return
				self.move()
				self.seeleft()
				return

	def gohome(self):
		self.seeleft()
		if self.obstacle():
			self.seeleft()
			self.move()
			self.seeright()
			self.move()
			self.move()
			self.seeright()
			self.move()
			self.move()
			self.seeright()
			self.move()
			self.seeleft()
			self.move()
			self.seeright()
			self.move()
			self.seeright()
			return
		self.move()
		self.seeright()
		if self.obstacle():
			self.seeleft()
			self.move()
			self.seeright()
			self.move()
			self.move()
			self.seeright()
			self.move()
			self.move()
			self.seeleft()
		self.move()
		if self.obstacle():
			self.seeleft()
			self.move()
			self.seeright()
			self.move()
			self.move()
			self.seeright()
			self.move()
			self.move()
			self.seeleft()
			return
		self.move()
		self.seeright()
		self.move()
		self.seeleft()
		return


A=robot(mv,av)
while not (A.mapend!=0 and len(A.history)+len(buildings)==(A.mapend+1)*(A.end+1)):
	if A.obstacle():
		A.check()
	elif A.move() == False:
		A.seeEast()
		if A.obstacle():
			A.check2()
		else:
			A.move()
			if A.pos[1]==0:
				A.seeright()
			else:
				A.seeleft()
A.seeWest()
A.seeright()
while A.pos[0]!=0:
	if -1<get_sensors()[1]<4:
		A.seeWest()
		if -1<get_sensors()[1]<4:
			A.seeleft()
			A.move()
			A.seeright()
			A.move()
		A.move()
		A.seeright()
	elif A.move() == False:
		break
A.seeWest()
while A.pos!=(0,0):
	if -1<get_sensors()[1]<4:
		A.gohome()
	elif A.move() == False:
		break
submit(lakes,buildings)





#### If you want to try moving around the map with your keyboard, uncomment the below lines 
import pygame
while True:
	pressed = pygame.key.get_pressed()
	if pressed[pygame.K_UP]: move_forward()
	if pressed[pygame.K_DOWN]: move_backward()
	if pressed[pygame.K_LEFT]: turn_left()
	if pressed[pygame.K_RIGHT]: turn_right()
	if pressed[pygame.K_n]: set_map((10,5), [(8,0), (4,9), (2,0), (3,3), (4,1)], [(7,2), (0,1), (2,3)])
	if pressed[pygame.K_c]: print(get_sensors())
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit("Closing...")