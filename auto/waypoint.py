from math import cos, sin, degrees
import matplotlib.pyplot as plt
x = 74.793630
y = 13.346027
way = []
r = 1
plt.plot(x,y,marker='o',markersize=5, color='red')
for i in range(0, 361, 60):
    cx = cos(degrees(i))*r/111035 + x
    cy = sin(degrees(i))*r/111035 + y
    a = []
    a.append(cx)
    a.append(cy)
    way.append(a)
    plt.plot(cx,cy,marker='o',markersize=3, color='green')
    plt.draw()
    plt.pause(0.001)
    
plt.show()
print(way)
