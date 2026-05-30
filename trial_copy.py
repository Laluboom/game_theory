import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

fig,ax=plt.subplots(figsize=(10,6))

x=np.arange(1,38)
y=np.random.rand(len(x))

N=20

def bar(pos):
    pos = int(pos)
    ax.clear()
    if pos+N > len(x): 
        n=len(x)-pos
    else:
        n=N
    X=x[pos:pos+n]
    Y=y[pos:pos+n]
    ax.bar(X,Y,width=0.7,align='edge',color='green',ecolor='black')

    for i,txt in enumerate(X):
       ax.annotate(txt, (X[i],Y[i]))

    ax.xaxis.set_ticks([])
    ax.yaxis.set_ticks([])

barpos = plt.axes([0.18, 0.05, 0.55, 0.03], facecolor="skyblue")
slider = Slider(barpos, 'Barpos', 0, len(x)-N, valinit=0)
slider.on_changed(bar)

bar(0)

plt.show()