from .base import Object, Space
from numpy import ndarray
from .units import *
from .utils import Vec
from math import pi

__all__ = ['Circle', 'Rectangle', 'Polygon', 'Regular']

# todo: circle에 반지름 선분 달아서 회전 알아보게 하기

class Circle(Object):
	def __init__(self, center: Quantity, radius: Quantity = 10 * m, *,
	             vel: Quantity = (0, 0) * m / s,
	             acc: Quantity = (0, 0) * m / s ** 2,
	             mass: Quantity = 1 * kg):
		super().__init__(center, vel=vel, acc=acc, mass=mass)
		
		if not radius.is_scalar(m):
			raise UnitError("Radius must be scalar in m.")
		
		self.radius = radius
	
	def update(self, space: "Space"):
		self.render(space)
		
		v_0 = self.vel
		x_0 = self.pos
		a = self.acc
		dt = 1 / (space.tps / 10)
		
		self.vel = v_0 + a * dt
		self.pos_0 = self.pos
		self.pos = x_0 + v_0 * dt + a * dt ** 2 / 2
	
	def render(self, space: "Space"):
		if self.render_object is None:
			p0, p1 = self.pos - self.radius, self.pos + self.radius
			self.render_object = space.create_oval(p0, p1, **self.configs)
		
		space.move(self, self.pos - self.pos_0)
	
	def __repr__(self):
		return f"Circle(pos={self.pos}, radius={self.radius}, mass={self.mass})"

class Rectangle(Object):
	def __init__(self, center: Quantity, size: Quantity, *,
	             vel: Quantity = (0, 0) * m / s,
	             acc: Quantity = (0, 0) * m / s ** 2,
	             mass: Quantity = 1 * kg):
		super().__init__(center, vel=vel, acc=acc, mass=mass)
		
		if not size.is_vector(m):
			raise UnitError("Size must be vector in m.")
		
		self.size = size
	
	@property
	def width(self) -> Quantity:
		return self.size.x
	
	@property
	def height(self) -> Quantity:
		return self.size.y
	
	def update(self, space: "Space"):
		self.render(space)
		
		v_0 = self.vel
		x_0 = self.pos
		a = self.acc
		dt = 1 / (space.tps / 10)
		
		self.vel = v_0 + a * dt
		self.pos_0 = self.pos
		self.pos = x_0 + v_0 * dt + a * dt ** 2 / 2
	
	def render(self, space: "Space"):
		if self.render_object is None:
			p0 = self.pos - Quantity.xy(self.width / 2, -self.height / 2)
			p1 = self.pos + Quantity.xy(self.width / 2, -self.height / 2)
			
			self.render_object = space.create_rectangle(p0, p1, **self.configs)
		
		space.move(self, self.pos - self.pos_0)
	
	def __repr__(self) -> str:
		return f"Rectangle(pos={self.pos}, width={self.width}, height={self.height}, mass={self.mass})"

class Polygon(Object):
	def __init__(self, points: tuple[Quantity] | list[Quantity] | ndarray[Quantity], *,
	             vel: Quantity = (0, 0) * m / s,
	             acc: Quantity = (0, 0) * m / s ** 2,
	             mass: Quantity = 1 * kg):
		super().__init__(sum(points) / len(points), vel=vel, acc=acc, mass=mass)
		
		if not all(p.is_vector(m) for p in points):
			raise UnitError("Points must be list of vector in m.")
		
		self.points = points
	
	def update(self, space: "Space"):
		self.render(space)
		
		v_0 = self.vel
		x_0 = self.pos
		a = self.acc
		dt = 1 / (space.tps / 10)
		
		self.vel = v_0 + a * dt
		self.pos_0 = self.pos
		self.pos = x_0 + v_0 * dt + a * dt ** 2 / 2
	
	def render(self, space: "Space"):
		if self.render_object is None:
			self.render_object = space.create_polygon(self.points, **self.configs)
		
		space.move(self, self.pos - self.pos_0)
	
	def __repr__(self) -> str:
		return f"Polygon(pos={self.pos}, points={self.points}, mass={self.mass})"

class Regular(Object):
	def __init__(self, center: Quantity, radius: Quantity = 10*m, *,
	             n: int,
	             vel: Quantity = (0, 0) * m / s,
	             acc: Quantity = (0, 0) * m / s ** 2,
	             mass: Quantity = 1 * kg):
		super().__init__(center, vel=vel, acc=acc, mass=mass)
		
		if not radius.is_scalar(m):
			raise UnitError("Radius must be scalar in m.")
		
		self.radius = radius
		self.n = n
	
	def update(self, space: "Space"):
		self.render(space)
		
		v_0 = self.vel
		x_0 = self.pos
		a = self.acc
		dt = 1 / (space.tps / 10)
		
		self.vel = v_0 + a * dt
		self.pos_0 = self.pos
		self.pos = x_0 + v_0 * dt + a * dt ** 2 / 2
	
	def render(self, space: "Space"):
		if self.render_object is None:
			the = 2*pi / self.n
			positions = [self.pos + Vec.P(self.radius.value, pi/2 + the*i)*m for i in range(self.n)]
			self.render_object = space.create_polygon(positions, **self.configs)
		
		space.move(self, self.pos - self.pos_0)
	
	def __repr__(self) -> str:
		return f"Regular(pos={self.pos}, n={self.n}, mass={self.mass})"
