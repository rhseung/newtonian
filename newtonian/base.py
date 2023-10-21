import numpy

from .units import *
from .utils import *
from tkinter import *
from time import sleep
from typing import Tuple
from abc import *

__all__ = ['Space', 'Object']

class Object(metaclass=ABCMeta):
	def __init__(self, mass: Quantity = 1*kg, *,
	             pos: Quantity = (0, 0)*m,
	             vel: Quantity = (0, 0)*m/s,
	             acc: Quantity = (0, 0)*m/s**2,
	             apos: Quantity = 0*rad,
	             avel: Quantity = 0*rad/s,
	             aacc: Quantity = 0*rad/s**2):
		
		if not mass.is_scalar(kg):
			raise UnitError("Mass must be in kg.")
		if not pos.is_vector(m):
			raise UnitError("Position must be vector in m.")
		if not vel.is_vector(m/s):
			raise UnitError("Velocity must be vector in m/s.")
		if not acc.is_vector(m/s**2):
			raise UnitError("Acceleration must be vector in m/s^2.")
		if not apos.is_scalar(rad):
			raise UnitError("Angular Position must be scalar in rad.")
		if not avel.is_scalar(rad/s):
			raise UnitError("Velocity must be scalar in rad/s.")
		if not aacc.is_scalar(rad/s**2):
			raise UnitError("Acceleration must be scalar in rad/s^2.")
		
		self.mass = mass
		
		self.pos_0 = pos
		self.pos = pos
		self.vel = vel
		self.acc = acc
		
		self.apos = apos
		self.avel = avel
		self.aacc = aacc
		
		self.render_object = None
		self.layer = 0
		
		self.configs = {
			'width': 1.,
			'outline': 'black',
			'fill': 'white'
		}
	
	def config(self, *, width: Quantity = None, outline: str = None, fill: str = None):
		if width is not None and width.is_scalar(m):
			self.configs['width'] = width.value
		if outline is not None:
			self.configs['outline'] = outline
		if fill is not None:
			self.configs['fill'] = fill
		
		return self
	
	@abstractmethod
	def update(self, space: "Space"):
		self.render(space)
	
	def render(self, space: "Space"):
		# todo: layer render how?
		#  - https://stackoverflow.com/questions/9576063/stacking-order-maintenance-in-tkinter/9576938#9576938
		#  또는 그냥 레이어를 생각하지 말고 충돌 그룹으로 생각하면 됨
		pass
	
	@abstractmethod
	def __repr__(self) -> str:
		return f"Object(pos={self.pos}, mass={self.mass})"
	
	def __str__(self):
		return self.__repr__()

class Space:
	def __init__(self, size: Tuple[int, int], *,
	             px: Quantity = 1 * m,
	             gravity: Quantity = (0, -9.80665) * m / s ** 2,
	             tps: Quantity = 60 / s):
		if gravity.unit != m / s ** 2 or gravity.is_scalar():
			raise UnitError("Gravity must be vector in m/s^2.")
		
		self.size = size
		self.px = px
		self.gravity = gravity
		self.tps = tps
		
		self.__master = Tk()
		self.__master.title('Newtonian Space')
		self.__master.resizable(False, False)
		self.__master.geometry(f"{self.size[0]}x{self.size[1]}")
		
		self.__canvas = Canvas(master=self.__master, width=self.size[0], height=self.size[1])
		self.__canvas.config(bg='white')
		self.__canvas.pack()
		
		self.__layers = Arrays()
	
	def config(self, *, screen_name: str = 'Newtonian Space', screen_icon: str = None, bg_color: str = None):
		if screen_name is not None:
			self.__master.title(screen_name)
		if screen_icon is not None:
			self.__master.iconbitmap(screen_icon)
		if bg_color is not None:
			self.__canvas.config(bg=bg_color)
		
		return self
	
	@property
	def width(self) -> float:
		return self.size[0]
	
	@property
	def height(self) -> float:
		return self.size[1]
	
	# todo: tick(dt, step=n)
	def tick(self):
		self.__master.update()
		# todo: loop, update 타임도 더해서 1/tps 가 되도록 = tps가 증가할수록 느려지는 현상 방지
		sleep(1 / self.tps.value)
	
	def is_destroyed(self):
		try:
			return not self.__master.winfo_exists()
		except TclError:
			return True
	
	def create_line(self, pos_0: Quantity, pos_1: Quantity, *args, **kw) -> int:
		if not pos_0.is_vector(m):
			raise UnitError("Position must be vector in m.")
		if not pos_1.is_vector(m):
			raise UnitError("Position must be vector in m.")
		
		pos_0 /= self.px
		pos_1 /= self.px
		
		return self.__canvas.create_line(pos_0.x, self.height - pos_0.y, pos_1.x, self.height - pos_1.y.value, *args,
		                                 **kw)
	
	def create_rectangle(self, pos_0: Quantity, pos_1: Quantity, *args, **kw) -> int:
		if not pos_0.is_vector(m):
			raise UnitError("Position must be vector in m.")
		if not pos_1.is_vector(m):
			raise UnitError("Position must be vector in m.")
		
		pos_0 /= self.px
		pos_1 /= self.px
		
		return self.__canvas.create_rectangle(pos_0.x, self.height - pos_0.y, pos_1.x, self.height - pos_1.y, *args,
		                                      **kw)
	
	def create_oval(self, pos_0: Quantity, pos_1: Quantity, *args, **kw) -> int:
		if not pos_0.is_vector(m):
			raise UnitError("Position must be vector in m.")
		if not pos_1.is_vector(m):
			raise UnitError("Position must be vector in m.")
		
		pos_0 /= self.px
		pos_1 /= self.px
		
		return self.__canvas.create_oval(pos_0.x, self.height - pos_0.y, pos_1.x, self.height - pos_1.y, *args, **kw)
	
	def create_text(self, pos: Quantity, *args, **kw) -> int:
		if not pos.is_vector(m):
			raise UnitError("Position must be vector in m.")
		
		pos /= self.px
		
		return self.__canvas.create_text(pos.x, self.height - pos.y, *args, **kw)
	
	def create_polygon(self, pos_list: tuple[Quantity] | list[Quantity] | numpy.ndarray[Quantity], *args, **kw) -> int:
		if not all(pos.is_vector(m) for pos in pos_list):
			raise UnitError("Position must be vector in m.")
		
		pos_list = [pos / self.px for pos in pos_list]
		return self.__canvas.create_polygon(*((pos.x, self.height - pos.y) for pos in pos_list), *args, **kw)
	
	def move(self, tag: int, d_pos: Quantity):
		if not d_pos.is_vector(m):
			raise UnitError("Position must be vector in m.")
		
		d_pos /= self.px
		
		self.__canvas.move(tag, d_pos.x, -d_pos.y)
	
	def coords(self, tag: int, pos_0: Quantity, pos_1: Quantity):
		if not pos_0.is_vector(m):
			raise UnitError("Position must be vector in m.")
		if not pos_1.is_vector(m):
			raise UnitError("Position must be vector in m.")
		
		pos_0 /= self.px
		pos_1 /= self.px
		
		self.__canvas.coords(tag, pos_0.x, self.height - pos_0.y, pos_1.x, self.height - pos_1.y)
	
	def __enter__(self):
		return self.__layers
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		pass
	
	def __iadd__(self, objects: Object | Tuple):
		if isinstance(objects, Object):
			objects = (objects,)
		else:
			objects = tuple(objects)
		
		layer_idx = 0
		for i, obj in enumerate(objects):
			if isinstance(obj, Object):
				self.__layers[layer_idx] += obj
				obj.layer = layer_idx
			else:   # tuple
				if i > 0:
					layer_idx += 1
				self.__layers[layer_idx] += obj
				for o in obj:
					o.layer = layer_idx
				layer_idx += 1
		
		return self
	
	def __bool__(self):
		return not self.is_destroyed()
	
	def __iter__(self):
		for arr in self.__layers:
			for obj in arr:
				yield obj
