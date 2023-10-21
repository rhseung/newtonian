import newtonian as nt
from newtonian.units import *

space = nt.Space((1000, 600), px=1.2*m, tps=120/s).config(screen_icon='test/icon.ico')

c1 = nt.Circle((200, 500)*m, 20*m, acc=space.gravity, avel=1*rad/s, vel=(3, 30)*m/s).config(fill='red', width=3*m)
c2 = nt.Circle((300, 500)*m, 15*m, acc=space.gravity, avel=-2*rad/s, vel=(5, 70)*m/s).config(fill='blue', width=5*m)
r1 = nt.Rectangle((400, 400)*m, (130, 20)*m, acc=space.gravity/10).config(fill='green', width=4*m)
p1 = nt.Polygon([(100, 400), (200, 300), (150, 280)]*m, acc=space.gravity/4).config(fill='purple', width=2*m)
t1 = nt.Regular((500, 400)*m, 20*m, n=3, acc=space.gravity/3).config(fill='yellow', width=2*m)
t2 = nt.Regular((600, 400)*m, 20*m, n=5, acc=space.gravity/3).config(fill='orange', width=2*m)
t3 = nt.Regular((700, 400)*m, 20*m, n=8, acc=space.gravity/3).config(fill='pink', width=2*m)

space += c1, c2, r1, p1, t1, t2, t3

while space:
	for obj in space:
		obj.update(space)
	
	space.tick()
