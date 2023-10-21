# import newtonian as nt
# from newtonian.units import *
# from numpy import array
# from math import pi, cos, sin, radians
#
# # n = 3
# # r = 3
# # the = 2*π / n
# #
# # p = nt.Vec.P(r, π/2)
# # p2 = nt.Vec.P(r, π/2 + the)
# # p3 = nt.Vec.P(r, π/2 + 2*the)
# #
# # l = [p, p2, p3] * m
# # print(l)
# # l = [_p / m for _p in l]
# # print(l)
# # print(*((pos.x, -pos.y) for pos in l))
#
# mass = 55.24*g
# k = 1.433*kg/s**2
# x = 0.06943*m
#
# Mass = 251.03*g
# μ = 0.00294
# gravity = 9.81*m/s**2
#
# a = (mass*gravity - k*x - μ*Mass*gravity)/(Mass - mass)
# T = mass*(gravity + a)
# print(T)
#
# print(2 * pi * (Mass / k) ** 0.5)
# print(2*pi * ((Mass + 500*g) / k)**0.5)

# ttk 테스트
import tkinter as tk

# 윈도우 생성
window = tk.Tk()
window.title("여러 개의 캔버스")

# 캔버스 1 생성
canvas1 = tk.Canvas(window, width=200, height=200, bg="rgba(0, 0, 0, 0.0)")
canvas1.pack()

# 캔버스 2 생성
canvas2 = tk.Canvas(window, width=200, height=200, bg="rgba(0, 0, 0, 0.0)")
canvas2.pack()

# 캔버스 3 생성
canvas3 = tk.Canvas(window, width=200, height=200, bg="rgba(0, 0, 0, 0.0)")
canvas3.pack()

# 각 캔버스에 그래픽 요소 추가 가능
canvas1.create_rectangle(10, 10, 100, 100, fill="blue")
canvas2.create_oval(10, 10, 100, 100, fill="red")
canvas3.create_line(10, 10, 100, 100, fill="green", width=5)

# 윈도우 실행
window.mainloop()

