from .base import Object, Space
from numpy import ndarray
from .units import *
from .utils import Vec
from math import pi, sin, cos, radians

__all__ = ['Circle', 'Rectangle', 'Polygon', 'Regular']

class Circle(Object):
	def __init__(self, center: Quantity, radius: Quantity = 10 * m, *,
	             vel: Quantity = (0, 0) * m / s,
	             acc: Quantity = (0, 0) * m / s ** 2,
	             apos: Quantity = 0*rad,
	             avel: Quantity = 0*rad/s,
	             aacc: Quantity = 0*rad/s**2,
	             mass: Quantity = 1 * kg):
		super().__init__(mass, pos=center, vel=vel, acc=acc, apos=apos, avel=avel, aacc=aacc)
		
		if not radius.is_scalar(m):
			raise UnitError("Radius must be scalar in m.")
		
		self.render_object2 = None
		self.apos_0 = self.apos
		self.is_radius_line = True
		self.radius = radius
	
	def config(self, *, width: Quantity = None, outline: str = None, fill: str = None, radius_line: bool = None):
		super().config(width=width, outline=outline, fill=fill)
		
		if radius_line is not None:
			self.is_radius_line = radius_line
		
		return self
	
	def update(self, space: "Space"):
		self.render(space)
		dt = 1 / (space.tps / 10)
		
		v_0 = self.vel
		x_0 = self.pos
		a = self.acc
		
		self.vel = v_0 + a*dt
		self.pos_0 = x_0
		self.pos = x_0 + v_0*dt + 1/2*a*dt**2
		
		ω_0 = self.avel
		θ_0 = self.apos
		α = self.aacc
		
		self.avel = ω_0 + α*dt
		self.apos_0 = θ_0
		self.apos = θ_0 + ω_0*dt + 1/2*α*dt**2
	
	def render(self, space: "Space"):
		if self.render_object is None:
			p0, p1 = self.pos - self.radius, self.pos + self.radius
			self.render_object = space.create_oval(p0, p1, **self.configs)
			
		if self.is_radius_line and self.render_object2 is None:
			self.render_object2 = space.create_line(
				self.pos,
                self.pos + self.radius * (cos(radians(self.apos.value)), sin(radians(self.apos.value))),
				width=self.configs['width']
            )
		
		space.coords(self.render_object2, self.pos, self.pos + self.radius * (cos(radians(self.apos.value)), sin(radians(self.apos.value))))
		space.move(self.render_object, self.pos - self.pos_0)
	
	def __repr__(self):
		return f"Circle(pos={self.pos}, radius={self.radius}, mass={self.mass})"

class Rectangle(Object):
	def __init__(self, center: Quantity, size: Quantity, *,
	             vel: Quantity = (0, 0) * m / s,
	             acc: Quantity = (0, 0) * m / s ** 2,
	             mass: Quantity = 1 * kg):
		super().__init__(mass, pos=center, vel=vel, acc=acc)
		
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
		
		space.move(self.render_object, self.pos - self.pos_0)
	
	def __repr__(self) -> str:
		return f"Rectangle(pos={self.pos}, width={self.width}, height={self.height}, mass={self.mass})"

class Polygon(Object):
	def __init__(self, points: tuple[Quantity] | list[Quantity] | ndarray[Quantity], *,
	             vel: Quantity = (0, 0)*m/s,
	             acc: Quantity = (0, 0)*m/s**2,
	             mass: Quantity = 1 * kg):
		super().__init__(mass, pos=sum(points) / len(points), vel=vel, acc=acc)
		
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
		
		space.move(self.render_object, self.pos - self.pos_0)
	
	def __repr__(self) -> str:
		return f"Polygon(pos={self.pos}, points={self.points}, mass={self.mass})"

class Regular(Object):
	def __init__(self, center: Quantity, radius: Quantity = 10*m, *,
	             n: int,
	             vel: Quantity = (0, 0) * m / s,
	             acc: Quantity = (0, 0) * m / s ** 2,
	             mass: Quantity = 1 * kg):
		super().__init__(mass, pos=center, vel=vel, acc=acc)
		
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
		
		space.move(self.render_object, self.pos - self.pos_0)
	
	def __repr__(self) -> str:
		return f"Regular(pos={self.pos}, n={self.n}, mass={self.mass})"
