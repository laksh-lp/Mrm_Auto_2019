import matplotlib.pyplot as plt
import numpy as np
import math as m

x = 2
y = 2
n = 0
while True:
	for i in range (0,360):
		angle = (i*np.pi)/180
		axes = plt.gca()
		axes.set_xlim([0,4])
		axes.set_ylim([0,4])
		dist = 1

		if i<=90 and i>=0:
			dy = np.sin(angle) + 2
			dx = (1 - (dy-2)**2)**0.5 + 2
			plt.arrow(x, y, dx-x, dy-y, width = 0.1, shape = 'full')
			plt.draw()
			plt.pause(0.005)
			plt.clf()

		elif i<=180 and i>90:
			dy = np.sin(angle) + 2
			dx = 2 - (1 - (dy-2)**2)**0.5
			plt.arrow(x, y, dx-x, dy-y, width = 0.1, shape = 'full')
			plt.draw()
			plt.pause(0.005)
			plt.clf()

		if i<=270 and i>180:
			dy = 2 - m.fabs(np.sin(angle))
			dx = 2 - (1 - (dy-2)**2)**0.5
			plt.arrow(x, y, dx-x, dy-y, width = 0.1, shape = 'full')
			plt.draw()
			plt.pause(0.005)
			plt.clf()

		elif i<360 and i>270:
			dy = 2 - m.fabs(np.sin(angle))
			dx = 2 + (1 - (dy-2)**2)**0.5
			plt.arrow(x, y, dx-x, dy-y, width = 0.1, shape = 'full')
			plt.draw()
			plt.pause(0.005)
			plt.clf()

plt.show()
